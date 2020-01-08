"""
The use of this file is to compile methods for different test types. This will make it easier to switch between
using different tests. Furthurmore, the creating of tests in this format will allow for them to be tested beforehand
"""

from ContinuousSampling import ContinuousSampling
from Hfss import Hfss
from MonteCarlo import MonteCarlo


class DataGenerationFunctions:
    """
    The use of this class is to facilitate the switching between functions by keeping certain parameters the same
    between each test type
    """

    def __init__(self):
        """
        Constructor used to initialize the class
        """
        self.all_parameter_names = ["a", "t_sub", "t_copper", "CylinderZ", "Crad", "Padding", "tau", "$phi_scan",
                                    "$theta_scan"]
        self.output_variables = ["re(S(FloquetPort1,FloquetPort1))", "im(S(FloquetPort1,FloquetPort1))",
                                 "re(S(FloquetPort1,FloquetPort2))", "im(S(FloquetPort1,FloquetPort2))"]
        self.output_folder = "C:\\Users\\denisshleifman\\Desktop\\4thYearProject\\test"
        self.testing = False

    def activate_test_mode(self):
        """
        Method used to activate the debug mode of the program. This is intended to stop any output from occuring
        """
        self.testing = True

    def basic_test_puck(self, o_design):
        """
        Basic theta sweep for the puck
        :param o_design:
        """
        parameter_names = ["$theta_scan"]
        parameter_units = ["deg"]
        test_object = Hfss(o_design, parameter_names, parameter_units, self.all_parameter_names, self.output_variables,
                           self.output_folder, 0, self.testing)
        test_object.set_frequency_sweep(1, 1.5, 10)

        theta = [20, 40]
        for x in theta:
            test_object.set_parameter_index(0, x)
            test_object.analyze_data()
        test_object.terminate()

    def geometry_puck_test(self, o_design):
        """
        Basic geometry and theta sweep for the puck
        :param o_design:
        """
        parameter_names = ["CylinderZ", "Crad", "$theta_scan"]
        parameter_units = ["mm", "mm", "deg"]
        test_object = Hfss(o_design, parameter_names, parameter_units, self.all_parameter_names, self.output_variables,
                           self.output_folder, 0, self.testing)

        test_object.set_frequency_sweep(1, 1.5, 10)
        theta = [20, 40]
        cylinder_z = [5, 6]
        crad = [2, 3]

        for x in cylinder_z:
            test_object.set_parameter_index(0, x)
            for y in crad:
                test_object.set_parameter_index(1, y)
                for z in theta:
                    test_object.set_parameter_index(2, z)
                    test_object.analyze_data()
        test_object.terminate()

    def geometry_puck_continuous(self, o_design):
        """
        Continous sampling method for puck
        :param o_design:
        """
        parameter_names = ["CylinderZ", "Crad", "$theta_scan"]
        parameter_units = ["mm", "mm", "deg"]
        test_object = Hfss(o_design, parameter_names, parameter_units, self.all_parameter_names, self.output_variables,
                           self.output_folder, 0, self.testing)
        test_object.set_frequency_sweep(1, 15, 25000)
        sampling = ContinuousSampling([1, 1, 0], [10, 10, 90], [0, 0, 0])

        while not sampling.check_finished():
            test_object.set_all_parameters(sampling.get_current_values())
            test_object.analyze_data()
            sampling.increment_values()
        test_object.terminate()

    def geometry_puck_monte(self, o_design):
        """
        Continous sampling method for puck
        :param o_design:
        """
        parameter_names = ["CylinderZ", "Crad", "$theta_scan"]
        parameter_units = ["mm", "mm", "deg"]
        test_object = Hfss(o_design, parameter_names, parameter_units, self.all_parameter_names, self.output_variables,
                           self.output_folder, 0, self.testing)
        test_object.set_frequency_sweep(1, 15, 25000)
        sampling = MonteCarlo([1, 1, 0], [9, 9, 85], [0, 0, 0])

        while not sampling.check_finished():
            test_object.set_all_parameters(sampling.get_current_values())
            test_object.analyze_data()
            sampling.increment_values()
        test_object.terminate()

    def puck_edges_continuous(self, o_design):
        """
        Test edges of sample space
        :param o_design:
        """
        parameter_names = ["CylinderZ", "Crad", "$theta_scan"]
        parameter_units = ["mm", "mm", "deg"]
        test_object = Hfss(o_design, parameter_names, parameter_units, self.all_parameter_names, self.output_variables,
                           self.output_folder, 1, self.testing)
        test_object.set_frequency_sweep(1, 15, 15)
        sampling = ContinuousSampling([1, 1, 0], [9, 9, 85], [0, 0, 0])
        sampling.set_max_iterations(1)
        counter = 0
        num_samples_skip = 0

        while not sampling.check_finished():
            counter += 1
            test_object.set_all_parameters(sampling.get_current_values())
            if counter > num_samples_skip:
                test_object.analyze_data()
            sampling.increment_values()
        test_object.terminate()

    def puck_edges_point(self, o_design):
        """
        Test edges of sample space
        :param o_design:
        """
        parameter_names = ["CylinderZ", "Crad", "$theta_scan"]
        parameter_units = ["mm", "mm", "deg"]
        test_object = Hfss(o_design, parameter_names, parameter_units, self.all_parameter_names,
                           self.output_variables, self.output_folder, 2, self.testing)
        test_object.set_frequency_sweep(1, 15, 15)
        test_object.set_all_parameters([8, 8, 60])
        test_object.analyze_data()
        test_object.terminate()
