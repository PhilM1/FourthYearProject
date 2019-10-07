# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2019.2.0
# 21:44:06  Oct 06, 2019
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Puck at 10GHz_script")
oDesign = oProject.SetActiveDesign("SRR2")
oModule = oDesign.GetModule("Optimetrics")
oModule.DeleteSetups(["ParametricSetup1"])
oModule.DeleteSetups(["ParametricSetup2"])
oModule = oDesign.GetModule("AnalysisSetup")
oModule.DeleteSetups(["Setup1"])
oProject.Save()
