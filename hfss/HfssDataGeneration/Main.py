"""
This is the main script for generating HFSS data
To call this script call the following command in the command prompt
"C:\Program Files\AnsysEM\AnsysEM19.5\Win64\ansysedt.exe"
-RunScriptAndExit C:\Users\denisshleifman\Desktop\4thYearProject\Main.py
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

fun.samplingMethod([1, 11, 100], [1, 1, 0], [9, 9, 85], [1, 1, 10.625], 3)
# fun.single_point()
# fun.test_sample_space_edges()
