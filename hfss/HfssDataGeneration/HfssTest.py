"""
This script was created to test the Hfss Class from another file
"""

from DataGenerationFunctions import DataGenerationFunctions
from Design import Design

fun = DataGenerationFunctions()
o_design = Design(True)
# fun.basic_test_puck(o_design)
# fun.geometry_puck_test(o_design)
# fun.geometry_puck_continuous(o_design)
fun.geometry_puck_monte(o_design)
# fun.puck_edges_continuous(o_design)
# fun.puck_edges_point(o_design)
