"""
The use of this file is to compile methods for different test types. This will make it easier to switch between
using different tests. Furthurmore, the creating of tests in this format will allow for them to be tested beforehand
"""

import re

from ContinuousSampling import ContinuousSampling
from Hfss import Hfss
# from MonteCarlo import MonteCarlo
from RandomList import RandomList


def generate_param_list(minimum, maximum, increment):
    """
    Function used to generate parameter list
    :param minimum: minimum value for each parameter
    :param maximum: maximum value for each parameter
    :param increment: increment value for each parameter
    :return: the parameter list
    """
    param_list = []
    curr = list(minimum)

    while True:
        param_list.append(list(curr))
        for n in range(len(minimum)):
            curr[n] += increment[n]
            if curr[n] > maximum[n]:
                if n == (len(minimum) - 1):
                    return param_list
                curr[n] = minimum[n]
            else:
                break


def remove_values_from_list(the_list, val):
    """
    Method used to remove values from the list
    :param the_list: list from which to remove
    :param val: value to remove
    :return: the list with the remove value
    """
    return [value for value in the_list if value != val]


def unique_list(list_in, output_folder):
    """
    Method used to cut down the list to not repeat already done points
    :param list_in: is the inputted 2D list. Each Row is a different point to sample
    :param output_folder: is the folder in which the output was generated.
    """

    file_object = open(Hfss.generate_output_filename(output_folder), "r")

    for line in file_object:
        tmp = line.split(",")
        start = False
        ls = []
        for n in range(len(tmp)):
            if tmp[n] == "OUTPUT":
                break
            if start:
                ls.append(float(re.findall(r'\d+(?:\.\d+)?', tmp[n])[0]))
            if tmp[n] == "INPUT":
                start = True
            list_in = remove_values_from_list(list_in, ls)

    file_object.close()
    return list_in


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
        # self.__output_folder = "C:\\Users\\eshlden\\Desktop\\4thYearProject"
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

    def samplingMethod(self, frequency, minimum, maximum, mode, method):
        """

        :param frequency:
        :param minimum:
        :param maximum:
        :param mode:
        :param method:
        """
        self.__activate_test_object(0)
        self.__test_object.set_frequency_sweep(frequency[0], frequency[1], frequency[2])

        if method == 1:
            self.__run_sampling_fcn(ContinuousSampling(minimum, maximum, mode))
        elif method == 2:
            pass
            # self.__run_sampling_fcn(MonteCarlo(minimum, maximum, mode))
        elif method == 3:
            self.__run_sampling_fcn(
                RandomList(unique_list(generate_param_list(minimum, maximum, mode), self.__output_folder)))

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
