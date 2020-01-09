"""
This file contains the Hfss class. This class is used as an interface with the HFSS program
"""
import os
import time


def generate_report_variables(all_parameter_names, parameter_names):
    """
    Function used to generate the report variables list
    :param all_parameter_names: is a list of all parameters
    :param parameter_names: is a list of all the parameters that will be changing
    :return: the report variables list
    """
    report_variables = ["Freq:=", ["All"]]
    for param in all_parameter_names:
        report_variables.append(param + ":=")
        if param in parameter_names:
            report_variables.append(["All"])
        else:
            report_variables.append(["Nominal"])
    return report_variables


def generate_optiparametric_sweep(variable, value, units):
    """
    Function used to generate the list needed for optiparametric sweeps
    :param variable: variable name
    :param value: value to set
    :param units: units of this value
    :return: the optiparametric sweep list
    """
    return ["NAME:SweepDefinition", "Variable:=", variable, "Data:=", str(value) + units, "OffsetF1:=", False,
            "Synchronize:=", 0]


def generate_optiparametric_setup(parameter_sweep_list):
    """
    Function used to generate the initializing array for the optiparametric setup
    :param parameter_sweep_list: list of parameters and their values
    :return: the initializing array for the optiparametric setup
    """
    return ["NAME:" + Hfss.OPTEMETRIC_SETUP_NAME, "IsEnabled:=", True,
            ["NAME:ProdOptiSetupDataV2", "SaveFields:=", False, "CopyMesh:=", False, "SolveWithCopiedMeshOnly:=", True],
            ["NAME:StartingPoint"], "Sim. Setups:=", [Hfss.ANALYSIS_SETUP_NAME], parameter_sweep_list,
            ["NAME:Sweep Operations"], ["NAME:Goals"]]


def generate_setup(frequency, min_passes, max_passes, max_delta_s):
    """
    Function used to generate the initializing array for the setup
    :param frequency: Solution frequency. This should be the maximum frequency being sweeped
    :param min_passes: Minimum number of passes
    :param max_passes: Maximum number of passes
    :param max_delta_s: Maximum change in Delta S
    :return: The array used to initialize the setup
    """
    return ["NAME:" + Hfss.ANALYSIS_SETUP_NAME, "AdaptMultipleFreqs:=", False, "Frequency:=", str(frequency) + "GHz",
            "MaxDeltaS:=", max_delta_s, "PortsOnly:=", False, "UseMatrixConv:=", False, "MaximumPasses:=", max_passes,
            "MinimumPasses:=", min_passes, "MinimumConvergedPasses:=", min_passes, "PercentRefinement:=", 30,
            "IsEnabled:=", True, "BasisOrder:=", 1, "DoLambdaRefine:=", True, "DoMaterialLambda:=", True,
            "SetLambdaTarget:=", False, "Target:=", 0.3333, "UseMaxTetIncrease:=", False, "PortAccuracy:=", 2,
            "UseABCOnPort:=", False, "SetPortMinMaxTri:=", False, "UseDomains:=", False, "UseIterativeSolver:=", False,
            "SaveRadFieldsOnly:=", False, "SaveAnyFields:=", True, "IESolverType:=", "Auto",
            "LambdaTargetForIESolver:=", 0.15, "UseDefaultLambdaTgtForIESolver:=", True]


def generate_sweep(min_freq, max_freq, range_count):
    """
    Function used to generate the array used to set the frequency sweep
    :param min_freq: Minimum frequency in GHz
    :param max_freq: Maximum frequency in GHz
    :param range_count: Number of data points to generate in the range
    :return: The array used to set the frequency sweep
    """
    return ["NAME:" + Hfss.SWEEP_NAME, "IsEnabled:=", True, "RangeType:=", "LinearCount", "RangeStart:=",
            str(min_freq) + "GHz", "RangeEnd:=", str(max_freq) + "GHz", "RangeCount:=", range_count, "Type:=",
            "Interpolating", "SaveFields:=", False, "SaveRadFields:=", False, "InterpTolerance:=", 0.5,
            "InterpMaxSolns:=", 250, "InterpMinSolns:=", 0, "InterpMinSubranges:=", 1, "ExtrapToDC:=", False,
            "InterpUseS:=", True, "InterpUsePortImped:=", False, "InterpUsePropConst:=", True,
            "UseDerivativeConvergence:=", False, "InterpDerivTolerance:=", 0.2, "UseFullBasis:=", True,
            "EnforcePassivity:=", True, "PassivityErrorTolerance:=", 0.0001]


class Hfss:
    """
    Class used to interface with HFSS models to simulate frequency sweeps with different geometric variables and
    incident angles for waves
    """

    ANALYSIS_SETUP_NAME = "Setup1"
    SWEEP_NAME = "Sweep"
    OPTEMETRIC_SETUP_NAME = "ParametricSetup1"
    REPORT_NAME = "S Parameter Plot 1"

    def __init__(self, o_design, parameter_names, parameter_units, all_parameter_names, output_variables,
                 output_folder, mode, testing):
        """
        Default constructor for this object
        :param o_design: oDesign is an object containing the project design
        :param parameter_names: List of names of the parameters that will be editable by this script
        :param parameter_units: List of the corresponding units
        :param all_parameter_names: This is the list of all the parameters
        :param output_variables: This is a list of the varables to output in the report
        :param output_folder: THis is the path to the output folder for the generated results
        :param mode: 0 for default, 1 for fast solving to test subspace, 2 for fast solving test space and don't clear
        :param testing: true to stop generation of output log
        results
        """
        self.mode = mode
        self.o_design = o_design
        self.output_older = output_folder
        self.output_variables = output_variables
        self.min_frequency = 0
        self.max_frequency = 0
        self.parameter_names = parameter_names
        self.parameter_units = parameter_units
        self.parameter_values = [0] * len(parameter_names)
        self.report_variables = generate_report_variables(all_parameter_names, parameter_names)
        self.module_analysis_setup = o_design.GetModule("AnalysisSetup")
        self.module_optimetrics = o_design.GetModule("Optimetrics")
        self.module_report_setup = o_design.GetModule("ReportSetup")
        self.module_analysis_setup.InsertSetup("HfssDriven", self.__create_setup_arr(1.5))
        self.module_analysis_setup.InsertFrequencySweep(Hfss.ANALYSIS_SETUP_NAME, generate_sweep(1, 15, 10))
        self.module_optimetrics.InsertSetup("OptiParametric",
                                            generate_optiparametric_setup(self.__generate_parameter_sweep_list()))
        self.__create_report()
        if self.mode == 0 and not self.testing:
            self.output_file_log = open(output_folder + os.path.sep + "outputFileLog.txt", "a")
        self.testing = testing

    def __create_setup_arr(self, frequency):
        """
        Method used to create an array for the setup depending on the mode and frequency selected
        :param frequency: is the frequency at which to set the solution (should be the maximum frequency)
        :return: the array used to initialize the setup
        """
        if self.mode == 0:
            return generate_setup(frequency, 2, 25, 0.005)
        else:
            return generate_setup(frequency, 1, 2, 0.5)

    def __create_report(self):

        """
        Method used to initialize the initial output report. The output data will be based off of the report data
        """
        self.module_report_setup.CreateReport(Hfss.REPORT_NAME, "Modal Solution Data", "Rectangular Plot",
                                              Hfss.ANALYSIS_SETUP_NAME + " : " + Hfss.SWEEP_NAME, ["Domain:=", "Sweep"],
                                              self.report_variables,
                                              ["X Component:=", "Freq", "Y Component:=", self.output_variables], [])

    def set_frequency_sweep(self, min_freq, max_freq, range_count):
        """
        Method used to set the frequency sweep
        :param min_freq: Minimum frequency in GHz
        :param max_freq: Maximum frequency in GHz
        :param range_count: Number of data points to generate in the range
        """
        self.min_frequency = min_freq
        self.max_frequency = max_freq
        self.module_analysis_setup.EditSetup(Hfss.ANALYSIS_SETUP_NAME, self.__create_setup_arr(max_freq))
        self.module_analysis_setup.EditFrequencySweep(Hfss.ANALYSIS_SETUP_NAME, Hfss.SWEEP_NAME,
                                                      generate_sweep(min_freq, max_freq, range_count))

    def set_parameter_name(self, parameter_name, value):
        """
        Method used to set a model parameter based on its name in the parameter list
        :param parameter_name: The name of the parameter in the parameter list
        :param value: The new parameter value
        """
        self.set_parameter_index(self.parameter_names.index(parameter_name), value)

    def set_parameter_index(self, parameter_index, value):
        """
        Method used to set a model parameter based on its index in the parameter list
        :param parameter_index: The index of the parameter being set in the parameter list
        :param value: The new parameter value
        """
        self.parameter_values[parameter_index] = value
        self.__set_parameter()

    def __generate_parameter_sweep_list(self):
        """
        Method used to set a model parameter based on its index in the parameter list
        :return: the list used with all the set parameters
        """
        sweep_list = ["NAME:Sweeps"]
        for x in range(len(self.parameter_values)):
            sweep_list.append(generate_optiparametric_sweep(self.parameter_names[x], self.parameter_values[x],
                                                            self.parameter_units[x]))
        return sweep_list

    def set_all_parameters(self, new_parameters):
        """
        Method used to set all parameters
        """
        self.parameter_values = new_parameters
        self.__set_parameter()

    def __set_parameter(self):
        """
        Method used to set all parameters in the program
        """

        self.module_optimetrics.EditSetup(Hfss.OPTEMETRIC_SETUP_NAME,
                                          generate_optiparametric_setup(self.__generate_parameter_sweep_list()))

    def __create_file_name(self):
        """
        Method used to create an auto-generated filename with parameters values in the filename
        :return: the full file name with path
        """
        file_name = str(int(time.time())) + ".csv"
        log_string = file_name + ",INPUT"
        for n in range(len(self.parameter_values)):
            log_string += "," + self.parameter_names[n] + "=" + str(self.parameter_values[n]) + self.parameter_units[n]
        log_string += ",OUTPUT"
        for n in range(len(self.output_variables)):
            log_string += "," + self.output_variables[n]

        self.output_file_log.write(log_string + "\n")
        self.output_file_log.flush()
        return self.output_older + os.path.sep + file_name

    def analyze_data(self):
        """
        Method used to analyze and export the data to a file
        """
        print("Performing analysis: " + str(self.parameter_values))
        self.module_optimetrics.EnableSetup(Hfss.OPTEMETRIC_SETUP_NAME, True)
        self.module_optimetrics.SolveSetup(Hfss.OPTEMETRIC_SETUP_NAME)
        if self.mode == 0 and not self.testing:
            self.module_report_setup.ExportToFile(Hfss.REPORT_NAME, self.__create_file_name())
        if self.mode != 2:
            self.o_design.DeleteFullVariation("All", False)
            self.module_report_setup.UpdateReports([Hfss.REPORT_NAME])

    def terminate(self):
        """
        Used to terminate the class. Closes the file type
        """
        if self.mode == 0 and not self.testing:
            self.output_file_log.close()
