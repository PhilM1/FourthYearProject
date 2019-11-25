"""
This is the main script for generating HFSS data
"""
import sys

sys.path.append("C:\\Users\\denisshleifman\\Desktop\\4thYearProject")
import ScriptEnv
import DataGenerationFunctions

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
try:
    oDesktop.OpenProject("C:\\Users\\denisshleifman\\Desktop\\4thYearProject\\Puck10GHz_Scripting.aedt")
except:
    print("Project already open")
o_project = oDesktop.SetActiveProject("Puck10GHz_Scripting")
o_design = o_project.SetActiveDesign("SRR2")
DataGenerationFunctions.basic_test_puck(o_design)
# DataGenerationFunctions.geometry_puck(o_design)
