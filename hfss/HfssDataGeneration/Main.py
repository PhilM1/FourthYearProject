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
fun = DataGenerationFunctions()
# fun.basic_test_puck(o_design)
# fun.geometry_puck_test(o_design)
# fun.geometry_puck_continuous(o_design)
fun.geometry_puck_monte(o_design)
# fun.puck_edges_continuous(o_design)
#fun.puck_edges_point(o_design)
