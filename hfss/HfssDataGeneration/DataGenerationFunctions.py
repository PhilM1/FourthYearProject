"""
The use of this file is to compile methods for different test types. This will make it easier to switch between
using different tests. Furthurmore, the creating of tests in this format will allow for them to be tested beforehand
"""

from ContinuousSampling import ContinuousSampling
from Hfss import Hfss
from MonteCarlo import MonteCarlo
from RandomList import RandomList


class DataGenerationFunctions:
    """
    The use of this class is to facilitate the switching between functions by keeping certain parameters the same
    between each test type
    """

    def __init__(self, o_design):
        """
        Constructor used to initialize the class
        :param o_design: is the HFSS object
        """
        self.__o_design = o_design
        self.__all_parameter_names = ["a", "t_sub", "t_copper", "CylinderZ", "Crad", "Padding", "tau", "$phi_scan",
                                      "$theta_scan"]
        self.__output_variables = ["re(S(FloquetPort1,FloquetPort1))", "im(S(FloquetPort1,FloquetPort1))",
                                   "re(S(FloquetPort1,FloquetPort2))", "im(S(FloquetPort1,FloquetPort2))"]
        self.__output_folder = "C:\\Users\\denisshleifman\\Desktop\\4thYearProject\\results2"
        self.__parameter_names = ["CylinderZ", "Crad", "$theta_scan"]
        self.__parameter_units = ["mm", "mm", "deg"]
        self.__testing = False
        self.__test_object = None

    def activate_test_mode(self):
        """
        Method used to activate the debug mode of the program. This is intended to stop any output from occuring
        """
        self.__testing = True

    def __run_sampling_fcn(self, sampling):
        """
        Function used to run the test once its setup
        :param sampling: is the sampling object used to sample the data points
        """
        while not sampling.check_finished():
            self.__test_object.set_all_parameters(sampling.get_current_values())
            self.__test_object.analyze_data()
            sampling.increment_values()
        self.__test_object.terminate()

    def __activate_test_object(self, mode):
        """
        Method used to activate the test object
        :param mode: 0 for default, 1 for fast solving to test subspace, 2 for fast solving test space and don't clear
        """
        self.__test_object = Hfss(self.__o_design, self.__parameter_names, self.__parameter_units,
                                  self.__all_parameter_names, self.__output_variables, self.__output_folder,
                                  self.__testing, mode)

    def random_list(self):
        """
        Continous sampling method for puck
        """
        self.__activate_test_object(0)
        self.__test_object.set_frequency_sweep(1, 15, 25000)
        param_list = []

        theta = [5.3125, 15.9375, 26.5625, 37.1875, 47.8125, 58.4375, 69.0625, 79.6875]
        cylinder_z = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        crad = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for x in cylinder_z:
            for y in crad:
                for z in theta:
                    param_list.append([x, y, z])
        self.__run_sampling_fcn(RandomList(param_list))

    def continuous_sampling(self):
        """
        Continous sampling method for puck
        """
        self.__activate_test_object(0)
        self.__test_object.set_frequency_sweep(1, 15, 25000)
        self.__run_sampling_fcn(ContinuousSampling([1, 1, 0], [10, 10, 90], [0, 0, 0]))

    def monte_carlo(self):
        """
        Continous sampling method for puck
        """
        self.__activate_test_object(0)
        self.__test_object.set_frequency_sweep(1, 15, 25000)
        self.__run_sampling_fcn(MonteCarlo([1, 1, 0], [9, 9, 85], [0, 0, 0]))

    def test_sample_space_edges(self):
        """
        Test edges of sample space
        """
        self.__activate_test_object(1)
        self.__test_object.set_frequency_sweep(1, 15, 15)
        sampling = ContinuousSampling([1, 1, 0], [9, 9, 85], [0, 0, 0])
        sampling.set_max_iterations(1)
        counter = 0
        num_samples_skip = 0

        while not sampling.check_finished():
            counter += 1
            self.__test_object.set_all_parameters(sampling.get_current_values())
            if counter > num_samples_skip:
                self.__test_object.analyze_data()
            sampling.increment_values()
        self.__test_object.terminate()

    def single_point(self):
        """
        Tests a single point in the sample space
        """
        self.__activate_test_object(2)
        self.__test_object.set_frequency_sweep(1, 15, 15)
        self.__test_object.set_all_parameters([8, 8, 60])
        self.__test_object.analyze_data()
        self.__test_object.terminate()
