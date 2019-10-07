# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2019.2.0
# 20:42:17  Oct 06, 2019
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Puck at 10GHz_myChanges")
oProject.Save()
oDesign = oProject.SetActiveDesign("SRR2")
oDesign.Analyze("Setup1 : Sweep")
oModule = oDesign.GetModule("AnalysisSetup")
oModule.EditFrequencySweep("Setup1", "Sweep", 
	[
		"NAME:Sweep",
		"IsEnabled:="		, True,
		"RangeType:="		, "LinearCount",
		"RangeStart:="		, "5GHz",
		"RangeEnd:="		, "15GHz",
		"RangeCount:="		, 100,
		"Type:="		, "Discrete",
		"SaveFields:="		, False,
		"SaveRadFields:="	, False,
		"ExtrapToDC:="		, False
	])
oModule.EditFrequencySweep("Setup1", "Sweep", 
	[
		"NAME:Sweep",
		"IsEnabled:="		, True,
		"RangeType:="		, "LinearCount",
		"RangeStart:="		, "5GHz",
		"RangeEnd:="		, "15GHz",
		"RangeCount:="		, 2,
		"Type:="		, "Discrete",
		"SaveFields:="		, False,
		"SaveRadFields:="	, False,
		"ExtrapToDC:="		, False
	])
oModule.EditFrequencySweep("Setup1", "Sweep", 
	[
		"NAME:Sweep",
		"IsEnabled:="		, True,
		"RangeType:="		, "LinearCount",
		"RangeStart:="		, "5GHz",
		"RangeEnd:="		, "15GHz",
		"RangeCount:="		, 2,
		"Type:="		, "Discrete",
		"SaveFields:="		, False,
		"SaveRadFields:="	, False,
		"ExtrapToDC:="		, False
	])
oModule.EditFrequencySweep("Setup1", "Sweep", 
	[
		"NAME:Sweep",
		"IsEnabled:="		, True,
		"RangeType:="		, "LinearCount",
		"RangeStart:="		, "5GHz",
		"RangeEnd:="		, "15GHz",
		"RangeCount:="		, 5,
		"Type:="		, "Discrete",
		"SaveFields:="		, False,
		"SaveRadFields:="	, False,
		"ExtrapToDC:="		, False
	])
