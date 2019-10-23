from Classes.Hfss import Hfss

import ScriptEnv

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Puck10GHz_Scripting")
oDesign = oProject.SetActiveDesign("SRR2")

# theta = [20,45,60,70]
testObject = Hfss(oDesign, "H:/ELEC4908Project/PUCK10GHz/Generated Data")
testObject.setFrequencySweep(1, 1.5, 10)

# for x in theta:
for x in range(20, 40, 5):
    testObject.setTheta(x)
    testObject.analyzeData()

testObject.terminate()