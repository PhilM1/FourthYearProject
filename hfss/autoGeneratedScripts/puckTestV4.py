# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2019.2.0
# 21:46:47  Oct 06, 2019
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Puck at 10GHz_script")
oDesign = oProject.SetActiveDesign("SRR2")
oModule = oDesign.GetModule("AnalysisSetup")
oModule.InsertSetup("HfssDriven", 
	[
		"NAME:Setup1",
		"AdaptMultipleFreqs:="	, False,
		"Frequency:="		, "15GHz",
		"MaxDeltaS:="		, 0.005,
		"PortsOnly:="		, False,
		"UseMatrixConv:="	, False,
		"MaximumPasses:="	, 25,
		"MinimumPasses:="	, 2,
		"MinimumConvergedPasses:=", 2,
		"PercentRefinement:="	, 30,
		"IsEnabled:="		, True,
		"BasisOrder:="		, 1,
		"DoLambdaRefine:="	, True,
		"DoMaterialLambda:="	, True,
		"SetLambdaTarget:="	, False,
		"Target:="		, 0.3333,
		"UseMaxTetIncrease:="	, False,
		"PortAccuracy:="	, 2,
		"UseABCOnPort:="	, False,
		"SetPortMinMaxTri:="	, False,
		"UseDomains:="		, False,
		"UseIterativeSolver:="	, False,
		"SaveRadFieldsOnly:="	, False,
		"SaveAnyFields:="	, True,
		"IESolverType:="	, "Auto",
		"LambdaTargetForIESolver:=", 0.15,
		"UseDefaultLambdaTgtForIESolver:=", True
	])
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
				"Variable:="		, "$theta_scan",
				"Data:="		, "LIN 0deg 45deg 5deg",
				"OffsetF1:="		, False,
				"Synchronize:="		, 0
			],
			[
				"NAME:SweepDefinition",
				"Variable:="		, "$phi_scan",
				"Data:="		, "15deg",
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
oModule = oDesign.GetModule("ReportSetup")
oModule.CreateReport("S Parameter Plot 1", "Modal Solution Data", "Rectangular Plot", "Setup1 : LastAdaptive", [], 
	[
		"Freq:="		, ["All"],
		"a:="			, ["Nominal"],
		"t_sub:="		, ["Nominal"],
		"t_copper:="		, ["Nominal"],
		"CylinderZ:="		, ["Nominal"],
		"Crad:="		, ["Nominal"],
		"Padding:="		, ["Nominal"],
		"tau:="			, ["Nominal"],
		"$phi_scan:="		, ["All"],
		"$theta_scan:="		, ["All"]
	], 
	[
		"X Component:="		, "Freq",
		"Y Component:="		, ["re(S(FloquetPort1,FloquetPort1))","im(S(FloquetPort1,FloquetPort1))","re(S(FloquetPort2,FloquetPort1))","im(S(FloquetPort2,FloquetPort1))","re(S(FloquetPort1,FloquetPort2))","im(S(FloquetPort1,FloquetPort2))","re(S(FloquetPort2,FloquetPort2))","im(S(FloquetPort2,FloquetPort2))"]
	], [])
oModule = oDesign.GetModule("AnalysisSetup")
oModule.InsertFrequencySweep("Setup1", 
	[
		"NAME:Sweep",
		"IsEnabled:="		, True,
		"RangeType:="		, "LinearCount",
		"RangeStart:="		, "1GHz",
		"RangeEnd:="		, "10GHz",
		"RangeCount:="		, 2,
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
oDesign.AnalyzeAllNominal()
oModule = oDesign.GetModule("Optimetrics")
oModule.EditSetup("ParametricSetup1", 
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
				"Variable:="		, "$theta_scan",
				"Data:="		, "0deg",
				"OffsetF1:="		, False,
				"Synchronize:="		, 0
			],
			[
				"NAME:SweepDefinition",
				"Variable:="		, "$phi_scan",
				"Data:="		, "15deg",
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
		"RangeEnd:="		, "10GHz",
		"RangeCount:="		, 2,
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
