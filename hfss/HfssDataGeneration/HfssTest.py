"""
This script was created to test the Hfss Class from another file
"""

from DataGenerationFunctions import DataGenerationFunctions
from Design import Design

fun = DataGenerationFunctions(Design(True))
fun.activate_test_mode()

fun.random_list()
# fun.continuous_sampling()
# fun.monte_carlo()
# fun.single_point()
# fun.test_sample_space_edges()
