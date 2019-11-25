"""
This file contains the Hfss class
"""
import os


class Hfss:
    """
    Class used to interface with HFSS models to simulate frequency sweeps with different geometric variables and
    incident angles for waves
    """

    ANALYSIS_SETUP_NAME = "Setup1"
    SWEEP_NAME = "Sweep"
    OPTEMETRIC_SETUP_NAME = "ParametricSetup1"
    REPORT_NAME = "S Parameter Plot 1"

    def __init__(self, o_design, parameter_names, parameter_units, report_variables, output_folder):
        """
        Default constructor for this object
        :param o_design: oDesign is an object containing the project design
        :param parameter_names: List of names of the parameters that will be editable by this script
        :param parameter_units: List of the corresponding units
        :param report_variables: This is the list of variables that is needed to generated the results
        Ex. ["Freq:=", ["All"],"a:=", ["Nominal"],"t_sub:=", ["Nominal"],"t_copper:=", ["Nominal"],
        "CylinderZ:=", ["Nominal"],"Crad:=", ["Nominal"],"Padding:=", ["Nominal"],"tau:=", ["Nominal"],
        "$phi_scan:=", ["All"],"$theta_scan:=", ["All"]]
        :param output_folder: THis is the path to the output folder for the generated results
        """
        self.o_design = o_design
        self.output_older = output_folder
        self.min_frequency = 0
        self.max_frequency = 0
        self.theta = 0
        self.phi = 0
        self.parameter_names = parameter_names
        self.parameter_units = parameter_units
        self.parameter_values = [0] * len(parameter_names)
        self.report_variables = report_variables
        self.module_analysis_setup = o_design.GetModule("AnalysisSetup")
        self.module_optimetrics = o_design.GetModule("Optimetrics")
        self.module_report_setup = o_design.GetModule("ReportSetup")
        self.__create_setup()
        self.__create_sweep()
        self.__create_opti_parametric()
        self.__create_report()

    def __create_setup(self):
        """
        Method used to initialize an initial setup
        """
        self.module_analysis_setup.InsertSetup("HfssDriven",
                                               [
                                                   "NAME:" + Hfss.ANALYSIS_SETUP_NAME,
                                                   "AdaptMultipleFreqs:=", False,
                                                   "Frequency:=", "1.5GHz",
                                                   "MaxDeltaS:=", 0.005,
                                                   "PortsOnly:=", False,
                                                   "UseMatrixConv:=", False,
                                                   "MaximumPasses:=", 25,
                                                   "MinimumPasses:=", 2,
                                                   "MinimumConvergedPasses:=", 2,
                                                   "PercentRefinement:=", 30,
                                                   "IsEnabled:=", True,
                                                   "BasisOrder:=", 1,
                                                   "DoLambdaRefine:=", True,
                                                   "DoMaterialLambda:=", True,
                                                   "SetLambdaTarget:=", False,
                                                   "Target:=", 0.3333,
                                                   "UseMaxTetIncrease:=", False,
                                                   "PortAccuracy:=", 2,
                                                   "UseABCOnPort:=", False,
                                                   "SetPortMinMaxTri:=", False,
                                                   "UseDomains:=", False,
                                                   "UseIterativeSolver:=", False,
                                                   "SaveRadFieldsOnly:=", False,
                                                   "SaveAnyFields:=", True,
                                                   "IESolverType:=", "Auto",
                                                   "LambdaTargetForIESolver:=", 0.15,
                                                   "UseDefaultLambdaTgtForIESolver:=", True
                                               ])

    def __create_sweep(self):
        """
        Method used to initialize an initial frequency sweep
        """
        self.module_analysis_setup.InsertFrequencySweep(Hfss.ANALYSIS_SETUP_NAME,
                                                        [
                                                            "NAME:Sweep",
                                                            "IsEnabled:=", True,
                                                            "RangeType:=", "LinearCount",
                                                            "RangeStart:=", "1GHz",
                                                            "RangeEnd:=", "1.5GHz",
                                                            "RangeCount:=", 10,
                                                            "Type:=", "Interpolating",
                                                            "SaveFields:=", False,
                                                            "SaveRadFields:=", False,
                                                            "InterpTolerance:=", 0.5,
                                                            "InterpMaxSolns:=", 250,
                                                            "InterpMinSolns:=", 0,
                                                            "InterpMinSubranges:=", 1,
                                                            "ExtrapToDC:=", False,
                                                            "InterpUseS:=", True,
                                                            "InterpUsePortImped:=", False,
                                                            "InterpUsePropConst:=", True,
                                                            "UseDerivativeConvergence:=", False,
                                                            "InterpDerivTolerance:=", 0.2,
                                                            "UseFullBasis:=", True,
                                                            "EnforcePassivity:=", True,
                                                            "PassivityErrorTolerance:=", 0.0001
                                                        ])

    def __create_opti_parametric(self):
        """
        Method used to initialize the optiParametric setup. This is used to control the incident angle of the plain
        waves (theta and phi)
        """
        self.module_optimetrics.InsertSetup("OptiParametric",
                                            [
                                                "NAME:" + Hfss.OPTEMETRIC_SETUP_NAME,
                                                "IsEnabled:=", True,
                                                [
                                                    "NAME:ProdOptiSetupDataV2",
                                                    "SaveFields:=", False,
                                                    "CopyMesh:=", False,
                                                    "SolveWithCopiedMeshOnly:=", True
                                                ],
                                                [
                                                    "NAME:StartingPoint"
                                                ],
                                                "Sim. Setups:=", [Hfss.ANALYSIS_SETUP_NAME],
                                                [
                                                    "NAME:Sweeps",
                                                    [
                                                        "NAME:SweepDefinition",
                                                        "Variable:=", "$phi_scan",
                                                        "Data:=", "0deg",
                                                        "OffsetF1:=", False,
                                                        "Synchronize:=", 0
                                                    ],
                                                    [
                                                        "NAME:SweepDefinition",
                                                        "Variable:=", "$theta_scan",
                                                        "Data:=", "0deg",
                                                        "OffsetF1:=", False,
                                                        "Synchronize:=", 0
                                                    ]
                                                ],
                                                [
                                                    "NAME:Sweep Operations"
                                                ],
                                                [
                                                    "NAME:Goals"
                                                ]
                                            ])

    def __create_report(self):
        """
        Method used to initialize the initial output report. The output data will be based off of the report data
        """
        self.module_report_setup.CreateReport(Hfss.REPORT_NAME, "Modal Solution Data", "Rectangular Plot",
                                              Hfss.ANALYSIS_SETUP_NAME + " : " + Hfss.SWEEP_NAME,
                                              [
                                                  "Domain:=", "Sweep"
                                              ],
                                              self.report_variables,
                                              [
                                                  "X Component:=", "Freq",
                                                  "Y Component:=", ["re(S(FloquetPort1,FloquetPort1))",
                                                                    "im(S(FloquetPort1,FloquetPort1))",
                                                                    "re(S(FloquetPort1,FloquetPort2))",
                                                                    "im(S(FloquetPort1,FloquetPort2))"]
                                              ], [])

    def set_frequency_sweep(self, min_freq, max_freq, range_count):
        """
        Method used to set the frequency sweep
        :param min_freq: Minimum frequency in GHz
        :param max_freq: Maximum frequency in GHz
        :param range_count: Number of data points to generate in the range
        """
        self.min_frequency = min_freq
        self.max_frequency = max_freq
        self.__set_frequency_solution(max_freq)
        self.module_analysis_setup.EditFrequencySweep(Hfss.ANALYSIS_SETUP_NAME, Hfss.SWEEP_NAME,
                                                      [
                                                          "NAME:" + Hfss.SWEEP_NAME,
                                                          "IsEnabled:=", True,
                                                          "RangeType:=", "LinearCount",
                                                          "RangeStart:=", str(min_freq) + "GHz",
                                                          "RangeEnd:=", str(max_freq) + "GHz",
                                                          "RangeCount:=", range_count,
                                                          "Type:=", "Interpolating",
                                                          "SaveFields:=", False,
                                                          "SaveRadFields:=", False,
                                                          "InterpTolerance:=", 0.5,
                                                          "InterpMaxSolns:=", 250,
                                                          "InterpMinSolns:=", 0,
                                                          "InterpMinSubranges:=", 1,
                                                          "ExtrapToDC:=", False,
                                                          "InterpUseS:=", True,
                                                          "InterpUsePortImped:=", False,
                                                          "InterpUsePropConst:=", True,
                                                          "UseDerivativeConvergence:=", False,
                                                          "InterpDerivTolerance:=", 0.2,
                                                          "UseFullBasis:=", True,
                                                          "EnforcePassivity:=", True,
                                                          "PassivityErrorTolerance:=", 0.0001
                                                      ])

    def __set_frequency_solution(self, frequency):
        """
        Method used to set the frequency at which the solution is created for. This should be the highest frequency of
        the frequency sweep.
        :param frequency: Input frequency solution
        """
        self.module_analysis_setup.EditSetup(Hfss.ANALYSIS_SETUP_NAME,
                                             [
                                                 "NAME:" + Hfss.ANALYSIS_SETUP_NAME,
                                                 "AdaptMultipleFreqs:=", False,
                                                 "Frequency:=", str(frequency) + "GHz",
                                                 "MaxDeltaS:=", 0.005,
                                                 "PortsOnly:=", False,
                                                 "UseMatrixConv:=", False,
                                                 "MaximumPasses:=", 25,
                                                 "MinimumPasses:=", 2,
                                                 "MinimumConvergedPasses:=", 2,
                                                 "PercentRefinement:=", 30,
                                                 "IsEnabled:=", True,
                                                 "BasisOrder:=", 1,
                                                 "DoLambdaRefine:=", True,
                                                 "DoMaterialLambda:=", True,
                                                 "SetLambdaTarget:=", False,
                                                 "Target:=", 0.3333,
                                                 "UseMaxTetIncrease:=", False,
                                                 "PortAccuracy:=", 2,
                                                 "UseABCOnPort:=", False,
                                                 "SetPortMinMaxTri:=", False,
                                                 "UseDomains:=", False,
                                                 "UseIterativeSolver:=", False,
                                                 "SaveRadFieldsOnly:=", False,
                                                 "SaveAnyFields:=", True,
                                                 "IESolverType:=", "Auto",
                                                 "LambdaTargetForIESolver:=", 0.15,
                                                 "UseDefaultLambdaTgtForIESolver:=", True
                                             ])

    def set_angle(self, theta, phi):
        """
        Method used to set the incident wave angles (theta and phi)
        :param theta: New incident theta angle
        :param phi: New incident phi angle
        """
        self.theta = theta
        self.phi = phi
        self.module_optimetrics.EditSetup(Hfss.OPTEMETRIC_SETUP_NAME,
                                          [
                                              "NAME:" + Hfss.OPTEMETRIC_SETUP_NAME,
                                              "IsEnabled:=", True,
                                              [
                                                  "NAME:ProdOptiSetupDataV2",
                                                  "SaveFields:=", False,
                                                  "CopyMesh:=", False,
                                                  "SolveWithCopiedMeshOnly:=", True
                                              ],
                                              [
                                                  "NAME:StartingPoint"
                                              ],
                                              "Sim. Setups:=", [Hfss.ANALYSIS_SETUP_NAME],
                                              [
                                                  "NAME:Sweeps",
                                                  [
                                                      "NAME:SweepDefinition",
                                                      "Variable:=", "$phi_scan",
                                                      "Data:=", str(phi) + "deg",
                                                      "OffsetF1:=", False,
                                                      "Synchronize:=", 0
                                                  ],
                                                  [
                                                      "NAME:SweepDefinition",
                                                      "Variable:=", "$theta_scan",
                                                      "Data:=", str(theta) + "deg",
                                                      "OffsetF1:=", False,
                                                      "Synchronize:=", 0
                                                  ]
                                              ],
                                              [
                                                  "NAME:Sweep Operations"
                                              ],
                                              [
                                                  "NAME:Goals"
                                              ]
                                          ])

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
        self.__set_parameter(self.parameter_values[parameter_index], value, self.parameter_units[parameter_index])

    def __set_parameter(self, parameter_name, value, unit):
        """
        Method used to set a model parameter
        :param parameter_name: The parameter name in the model
        :param value: The new value
        :param unit: The parameter unit
        """
        self.o_design.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:LocalVariableTab",
                    [
                        "NAME:PropServers",
                        "LocalVariables"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:", parameter_name,
                            "Value:=", str(value) + unit
                        ]
                    ]
                ]
            ])

    def __create_file_name(self):
        """
        Method used to create an auto-generated filename with parameters values in the filename
        :return: the full file name with path
        """
        file_path = self.output_older + os.path.sep + "sParam_" + str(self.theta) + "_" + str(self.phi)
        for x in self.parameter_values:
            file_path += "_" + str(x)
        file_path += "_" + str(self.min_frequency) + "_" + str(self.max_frequency) + ".csv"
        return file_path

    def __create_file_format_string(self):
        """
        Method used to create a string representing the file format. This string shows the order of each variable in
        the autogenerated data files
        :return: the formatted string with the list of variables
        """
        file_format_string = "sParam_" + "theta_phi"
        for x in self.parameter_names:
            file_format_string += "_" + x
        file_format_string += "_minFreq_maxFreq.csv"
        return file_format_string

    def analyze_data(self):
        """
        Method used to analyze and export the data to a file
        """
        self.module_optimetrics.EnableSetup(Hfss.OPTEMETRIC_SETUP_NAME, True)
        self.module_optimetrics.SolveSetup(Hfss.OPTEMETRIC_SETUP_NAME)
        self.module_report_setup.ExportToFile(Hfss.REPORT_NAME, self.__create_file_name())
        self.o_design.DeleteFullVariation("All", False)
        self.module_report_setup.UpdateReports([Hfss.REPORT_NAME])

    def terminate(self):
        """
        Method used to terminate this object. This method outputs information pertaining to the output files generated.
        """

        print("Files outputted to" + self.output_older)
        print("File format: " + self.__create_file_format_string())
