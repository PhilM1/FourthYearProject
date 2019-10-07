# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2019.2.0
# 22:00:17  Oct 06, 2019
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("60GHZHuygens_Tester")
oDesign = oProject.SetActiveDesign("Unit_Cell_Rogers")
oModule = oDesign.GetModule("ReportSetup")
oModule.ExportToFile("S Parameter Plot 1", "H:/ELEC4908Project/data/S Parameter Plot test.csv")
