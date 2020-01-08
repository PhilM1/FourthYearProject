"""
This file contains the ContinuousSampling Class
"""


class ContinuousSampling:
    """
    Class is used as a parent method for all sampling methods. It is intended to standardize the interaction of all of
    these types so that they can be easily used together. This class is not intended to be used on its own
    """

    def __init__(self, minimums, maximums, mode):
        """
        Constructor for the ContinuousSampling Class. Initializes all variables, sets the max step to be disables
        :param minimums: minimum values for each variable
        :param maximums: maximum value for each variable
        :param mode: 0 for linear, 1 for logarithmic, 2 for gaussian for each variable
        """
        self.numVars = len(minimums)
        self.minimums = minimums
        self.maximums = maximums
        self.mode = mode
        self.iterations = 0
        self.max_iterations = -1

    def set_max_iterations(self, new_max_iterations):
        """
        Sets a maximum number of iterations  value. This will allow for a check to see if the maximum iterations has
        been reached. Set to -1 to disable
        :param new_max_iterations: the new maximum step value
        """
        self.max_iterations = new_max_iterations

    def check_finished(self):
        """
        Method checks to see if the maximum iterations has been reached
        :return: true if the maximum iterations has been reached
        """
        if self.max_iterations == -1:
            return False
        return self.iterations > self.max_iterations

    def increment_values(self):
        """
        Method used to increment values. This method is overidden by child classes
        """
        pass

    def get_current_values(self):
        """
        Getter for the current values
        :return: the current values
        """
        return self.current_values
