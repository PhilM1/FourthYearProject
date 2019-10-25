"""
This is the main script for generating HFSS data
"""
import ScriptEnv
import DataGenerationFunctions
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
o_project = oDesktop.SetActiveProject("Puck10GHz_Scripting")
o_design = o_project.SetActiveDesign("SRR2")
DataGenerationFunctions.basic_test_puck(o_design)
