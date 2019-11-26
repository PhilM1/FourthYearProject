"""
This class contains the continuous sampling class. This class is used to interface with the Hfss class in order to
continuously sample a certain sample space
"""
import math


def calculateLinear(minimum, maximum, count, step):
    """
    Function to calculate the current value to set using a linear method
    :param minimum: minimum value
    :param maximum: maximum value
    :param count: current count
    :param step: current step
    :return: current value to set
    """
    return minimum + count * (maximum - minimum) / float(step)


def calculateLog(minimum, maximum, count, step):
    """
    Function to calculate the current value to set using a log method
    :param minimum: minimum value
    :param maximum: maximum value
    :param count: current count
    :param step: current step
    :return: current value to set
    """
    if minimum != 0:
        return minimum * math.pow(maximum / float(minimum), count / float(step))
    return math.pow(maximum + 1, count / float(step)) - 1


class ContinuousSampling:
    """
    This class is used to continuously sample a certain space such that as time goes on the granularity increases. This
    works by sampling the space at a certain granularity, then when finished, the granularity will double and the
    process will repeat. The class is written such that it never samples the same point twice.
    """

    def __init__(self, minimums, maximums, mode):
        """
        Constructor for the ContinuousSampling Class. Initializes all variables, sets the max step to be disables
        :param minimums: minimum values for each variable
        :param maximums: maximum value for each variable
        :param mode: 0 for linear, 1 for logarithmic
        """
        self.numVars = len(minimums)
        self.minimums = minimums
        self.maximums = maximums
        self.mode = mode
        self.step = 1
        self.count = [0] * self.numVars
        self.current_values = []
        for n in minimums:
            self.current_values.append(n)
        self.max_step = -1

    def set_max_step(self, new_max_step):
        """
        Sets a maximum step value. This will allow for a check to see if the maximum step has been reached.
        Set to -1 to disable
        :param new_max_step: the new maximum step value
        """
        self.max_step = new_max_step

    def check_finished(self):
        """
        Method checks to see if the maximum step has been reached
        :return: true if the maximum step has been reached
        """
        if self.max_step == -1:
            return False
        return self.step > self.max_step

    def __check_value_done(self):
        """
        Method used to check if a certain value has already been outputted in previous steps
        :return: True if the value has already been outputted
        """
        if self.step == 1:
            return False
        for n in self.count:
            if n % 2 != 0:
                return False
        return True

    def __overflow(self):
        """
        Method used to handle an overflow of the first count element. If so the method will search for another element
        to increment. If unable to find another one, the step will be incremented and the count list will be reset
        :return: used to exit out of the method early if element is found to increment
        """
        for n in range(self.numVars):
            if self.count[n] < self.step:
                self.count[n] += 1
                self.count[0] = 0
                return
        self.count = [0] * self.numVars
        self.step *= 2

    def __calc_current_values(self):
        """
        Method used to update the current values (depending on the mode selected)
        """
        for n in range(self.numVars):
            if self.mode == 0:
                self.current_values[n] = calculateLinear(self.minimums[n], self.maximums[n], self.count[n], self.step)
            elif self.mode == 1:
                self.current_values[n] = calculateLog(self.minimums[n], self.maximums[n], self.count[n], self.step)

    def increment_values(self):
        """
        Method used to increment values. Will ensure granularity increases and will increment until new values are found
        :return: void
        """
        self.count[0] += 1
        if self.count[0] - 1 == self.step:
            self.__overflow()

        self.__calc_current_values()

        if self.__check_value_done():
            self.increment_values()

    def get_current_values(self):
        """
        Getter for the current values
        :return: the current values
        """
        return self.current_values