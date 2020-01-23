"""
This is the main script for generating HFSS data
"""
import sys

sys.path.append("C:\\Users\\denisshleifman\\Desktop\\4thYearProject")
import ScriptEnv
from DataGenerationFunctions import DataGenerationFunctions

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
try:
    oDesktop.OpenProject("C:\\Users\\denisshleifman\\Desktop\\4thYearProject\\Puck10GHz_Scripting.aedt")
except:
    print("Project already open")
o_project = oDesktop.SetActiveProject("Puck10GHz_Scripting")
o_design = o_project.SetActiveDesign("SRR2")
fun = DataGenerationFunctions(o_design)

fun.random_list()
# fun.continuous_sampling()
# fun.loop_test()
# fun.monte_carlo()
# fun.single_point()
# fun.test_sample_space_edges()
