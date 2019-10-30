# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2019.2.0
# 14:07:43  Oct 30, 2019
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Puck at 10GHz (1)")
oDesign = oProject.SetActiveDesign("SRR2")
oDesign.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:LocalVariableTab",
			[
				"NAME:PropServers", 
				"LocalVariables"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:CylinderZ",
					"Value:="		, "3.08mm"
				],
				[
					"NAME:Crad",
					"Value:="		, "6.62mm"
				]
			]
		]
	])
oModule = oDesign.GetModule("ReportSetup")
oModule.DeleteReports(["S Parameter Plot 1"])
oModule.DeleteReports(["S Parameter Plot 2"])
oModule.DeleteReports(["S Parameter Plot 3"])
oModule = oDesign.GetModule("Optimetrics")
oModule.DeleteSetups(["ParametricSetup1"])
oModule.DeleteSetups(["ParametricSetup2"])
oModule = oDesign.GetModule("ReportSetup")
oModule.CreateReport("S Parameter Plot 1", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
	[
		"Domain:="		, "Sweep"
	], 
	[
		"Freq:="		, ["All"],
		"a:="			, ["Nominal"],
		"t_sub:="		, ["Nominal"],
		"t_copper:="		, ["Nominal"],
		"CylinderZ:="		, ["Nominal"],
		"Crad:="		, ["Nominal"],
		"Padding:="		, ["Nominal"],
		"tau:="			, ["Nominal"],
		"$phi_scan:="		, ["Nominal"],
		"$theta_scan:="		, ["Nominal"]
	], 
	[
		"X Component:="		, "Freq",
		"Y Component:="		, ["re(S(FloquetPort1,FloquetPort1))","im(S(FloquetPort1,FloquetPort1))"]
	], [])
oModule.CreateReport("S Parameter Plot 2", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
	[
		"Domain:="		, "Sweep"
	], 
	[
		"Freq:="		, ["All"],
		"a:="			, ["Nominal"],
		"t_sub:="		, ["Nominal"],
		"t_copper:="		, ["Nominal"],
		"CylinderZ:="		, ["Nominal"],
		"Crad:="		, ["Nominal"],
		"Padding:="		, ["Nominal"],
		"tau:="			, ["Nominal"],
		"$phi_scan:="		, ["Nominal"],
		"$theta_scan:="		, ["Nominal"]
	], 
	[
		"X Component:="		, "Freq",
		"Y Component:="		, ["re(S(FloquetPort1,FloquetPort2))","im(S(FloquetPort1,FloquetPort2))"]
	], [])
oModule = oDesign.GetModule("Optimetrics")
oModule.InsertSetup("OptiParametric", 
	[
		"NAME:ParametricSetup1",
		"IsEnabled:="		, True,
		[
			"NAME:ProdOptiSetupDataV2",
			"SaveFields:="		, False,
			"CopyMesh:="		, False,
			"SolveWithCopiedMeshOnly:=", True
		],
		[
			"NAME:StartingPoint"
		],
		"Sim. Setups:="		, ["Setup1"],
		[
			"NAME:Sweeps",
			[
				"NAME:SweepDefinition",
				"Variable:="		, "$phi_scan",
				"Data:="		, "90deg",
				"OffsetF1:="		, False,
				"Synchronize:="		, 0
			],
			[
				"NAME:SweepDefinition",
				"Variable:="		, "$theta_scan",
				"Data:="		, "0deg",
				"OffsetF1:="		, False,
				"Synchronize:="		, 0
			]
		],
		[
			"NAME:Sweep Operations"
		],
		[
			"NAME:Goals"
		]
	])
oModule = oDesign.GetModule("AnalysisSetup")
oModule.EditFrequencySweep("Setup1", "Sweep", 
	[
		"NAME:Sweep",
		"IsEnabled:="		, True,
		"RangeType:="		, "LinearCount",
		"RangeStart:="		, "1GHz",
		"RangeEnd:="		, "1.5GHz",
		"RangeCount:="		, 1000,
		"Type:="		, "Interpolating",
		"SaveFields:="		, False,
		"SaveRadFields:="	, False,
		"InterpTolerance:="	, 0.5,
		"InterpMaxSolns:="	, 250,
		"InterpMinSolns:="	, 0,
		"InterpMinSubranges:="	, 1,
		"ExtrapToDC:="		, False,
		"InterpUseS:="		, True,
		"InterpUsePortImped:="	, False,
		"InterpUsePropConst:="	, True,
		"UseDerivativeConvergence:=", False,
		"InterpDerivTolerance:=", 0.2,
		"UseFullBasis:="	, True,
		"EnforcePassivity:="	, True,
		"PassivityErrorTolerance:=", 0.0001
	])
oProject.Save()
oDesign.Analyze("Setup1 : Sweep")
