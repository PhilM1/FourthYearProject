"""
This file contains the MonteCarlo Class
"""
import math

import numpy as np

from SamplingMethod import SamplingMethod


def generate_random_value(minimum, maximum, mode):
    """
    Function used to generate a random number using the proper distribution
    :param minimum: minimum value
    :param maximum: maximum value
    :param mode: 0 for linear, 1 for logarithmic, 2 for gaussian centered at the middle between min and max.
    :return: the random number
    """
    if mode == 0:
        return np.random.uniform(minimum, maximum)
    elif mode == 1:
        math.pow(np.random.random(), 2) * (maximum - minimum) + minimum
    elif mode == 2:
        condition = True
        val = (minimum + maximum) / 2
        while condition:
            val = np.random.normal((minimum + maximum) / 2, (maximum - minimum) / 6)
            condition = val < minimum or val > maximum
        return val


class MonteCarlo(SamplingMethod):
    """
    Class is used to interface with the hfss class. This class will allow the creation of new data points using the
    monte carlo method.
    """

    def __init__(self, minimums, maximums, mode):
        """
        Constructor for the MonteCarlo Class. Initializes all variables, sets the max step to be disables
        :param minimums: minimum values for each variable
        :param maximums: maximum value for each variable
        :param mode: 0 for linear, 1 for logarithmic, 2 for gaussian for each variable
        """
        SamplingMethod.__init__(self, minimums, maximums, mode)
        self.increment_values()

    def increment_values(self):
        """
        Method used to increment the current values
        """
        if self.check_finished():
            return

        self.iterations += 1
        for n in range(self.numVars):
            self.current_values[n] = generate_random_value(self.minimums[n], self.maximums[n], self.mode[n])
