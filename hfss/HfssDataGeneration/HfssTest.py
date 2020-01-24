"""
This script was created to test the Hfss Class from another file
"""

from DataGenerationFunctions import DataGenerationFunctions
from Design import Design

fun = DataGenerationFunctions(Design(True))
fun.activate_test_mode()

fun.samplingMethod([1, 11, 100], [1, 1, 0], [9, 9, 85], [1, 1, 10.625], 3)
# fun.single_point()
# fun.test_sample_space_edges()
