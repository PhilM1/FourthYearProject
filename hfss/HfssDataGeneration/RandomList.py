"""
This file contains the Random List Class
"""
import random

from SamplingMethod import SamplingMethod


class RandomList(SamplingMethod):
    """
    Class is used to interface with the hfss class. This class will allow for a list of data points to be run, however,
    the execution of the order of this list will be random
    """

    def __init__(self, list_in):
        """
        Constructor for the RandomList Class
        :param list_in: is the inputted 2D list. Each Row is a different point to sample
        """
        SamplingMethod.__init__(self, [], [], [])
        random.shuffle(list_in)
        self.list = list_in
        self.num_elements = len(self.list)
        self.increment_values()
        if self.max_iterations == -1 or self.max_iterations > len(self.list):
            self.set_max_iterations(len(self.list))

    def set_max_iterations(self, new_max_iterations):
        """
        Sets a maximum number of iterations  value. This will allow for a check to see if the maximum iterations has
        been reached. Set to -1 to disable
        :param new_max_iterations: the new maximum step value
        """
        if new_max_iterations > len(self.list):
            self.max_iterations = len(self.list)
        else:
            self.max_iterations = new_max_iterations

    def increment_values(self):
        """
        Method used to increment the current values
        """
        self.iterations += 1

        if self.iterations >= self.num_elements:
            return

        self.current_values = self.list[self.iterations]
