class Hfss:
    ANALYSIS_SETUP_NAME = "Setup1"
    SWEEP_NAME = "Sweep"
    OPTEMETRIC_SETUP_NAME = "ParametricSetup1"
    REPORT_NAME = "S Parameter Plot 1"

    def __init__(self, oDesign, outputFolder):
        self.oDesign = oDesign
        self.outputFolder = outputFolder
        self.minFrequency = 0
        self.maxFrequency = 0
        self.theta = 0
        self.oModuleAnalysisSetup = oDesign.GetModule("AnalysisSetup")
        self.oModuleOptimetrics = oDesign.GetModule("Optimetrics")
        self.oModuleReportSetup = oDesign.GetModule("ReportSetup")
        self.createSetup()
        self.createSweep()
        self.createOptiParametric()
        self.createReport()

    def createSetup(self):
        self.oModuleAnalysisSetup.InsertSetup("HfssDriven",
                                              [
                                                  "NAME:" + Hfss.ANALYSIS_SETUP_NAME,
                                                  "AdaptMultipleFreqs:=", False,
                                                  "Frequency:=", "1.5GHz",
                                                  "MaxDeltaS:=", 0.005,
                                                  "PortsOnly:=", False,
                                                  "UseMatrixConv:=", False,
                                                  "MaximumPasses:=", 25,
                                                  "MinimumPasses:=", 2,
                                                  "MinimumConvergedPasses:=", 2,
                                                  "PercentRefinement:=", 30,
                                                  "IsEnabled:=", True,
                                                  "BasisOrder:=", 1,
                                                  "DoLambdaRefine:=", True,
                                                  "DoMaterialLambda:=", True,
                                                  "SetLambdaTarget:=", False,
                                                  "Target:=", 0.3333,
                                                  "UseMaxTetIncrease:=", False,
                                                  "PortAccuracy:=", 2,
                                                  "UseABCOnPort:=", False,
                                                  "SetPortMinMaxTri:=", False,
                                                  "UseDomains:=", False,
                                                  "UseIterativeSolver:=", False,
                                                  "SaveRadFieldsOnly:=", False,
                                                  "SaveAnyFields:=", True,
                                                  "IESolverType:=", "Auto",
                                                  "LambdaTargetForIESolver:=", 0.15,
                                                  "UseDefaultLambdaTgtForIESolver:=", True
                                              ])

    def createSweep(self):
        self.oModuleAnalysisSetup.InsertFrequencySweep(Hfss.ANALYSIS_SETUP_NAME,
                                                       [
                                                           "NAME:Sweep",
                                                           "IsEnabled:=", True,
                                                           "RangeType:=", "LinearCount",
                                                           "RangeStart:=", "1GHz",
                                                           "RangeEnd:=", "1.5GHz",
                                                           "RangeCount:=", 10,
                                                           "Type:=", "Interpolating",
                                                           "SaveFields:=", False,
                                                           "SaveRadFields:=", False,
                                                           "InterpTolerance:=", 0.5,
                                                           "InterpMaxSolns:=", 250,
                                                           "InterpMinSolns:=", 0,
                                                           "InterpMinSubranges:=", 1,
                                                           "ExtrapToDC:=", False,
                                                           "InterpUseS:=", True,
                                                           "InterpUsePortImped:=", False,
                                                           "InterpUsePropConst:=", True,
                                                           "UseDerivativeConvergence:=", False,
                                                           "InterpDerivTolerance:=", 0.2,
                                                           "UseFullBasis:=", True,
                                                           "EnforcePassivity:=", True,
                                                           "PassivityErrorTolerance:=", 0.0001
                                                       ])

    def createOptiParametric(self):
        self.oModuleOptimetrics.InsertSetup("OptiParametric",
                                            [
                                                "NAME:" + Hfss.OPTEMETRIC_SETUP_NAME,
                                                "IsEnabled:=", True,
                                                [
                                                    "NAME:ProdOptiSetupDataV2",
                                                    "SaveFields:=", False,
                                                    "CopyMesh:=", False,
                                                    "SolveWithCopiedMeshOnly:=", True
                                                ],
                                                [
                                                    "NAME:StartingPoint"
                                                ],
                                                "Sim. Setups:=", [Hfss.ANALYSIS_SETUP_NAME],
                                                [
                                                    "NAME:Sweeps",
                                                    [
                                                        "NAME:SweepDefinition",
                                                        "Variable:=", "$theta_scan",
                                                        "Data:=", "0deg",
                                                        "OffsetF1:=", False,
                                                        "Synchronize:=", 0
                                                    ]
                                                ],
                                                [
                                                    "NAME:Sweep Operations"
                                                ],
                                                [
                                                    "NAME:Goals"
                                                ]
                                            ])

    def createReport(self):
        self.oModuleReportSetup.CreateReport(Hfss.REPORT_NAME, "Modal Solution Data", "Rectangular Plot",
                                             Hfss.ANALYSIS_SETUP_NAME + " : " + Hfss.SWEEP_NAME,
                                             [
                                                 "Domain:=", "Sweep"
                                             ],
                                             [
                                                 "Freq:=", ["All"],
                                                 "a:=", ["Nominal"],
                                                 "t_sub:=", ["Nominal"],
                                                 "t_copper:=", ["Nominal"],
                                                 "CylinderZ:=", ["Nominal"],
                                                 "Crad:=", ["Nominal"],
                                                 "Padding:=", ["Nominal"],
                                                 "tau:=", ["Nominal"],
                                                 "$phi_scan:=", ["Nominal"],
                                                 "$theta_scan:=", ["All"]
                                             ],
                                             [
                                                 "X Component:=", "Freq",
                                                 "Y Component:=", ["re(S(FloquetPort1,FloquetPort1))",
                                                                   "im(S(FloquetPort1,FloquetPort1))",
                                                                   "re(S(FloquetPort1,FloquetPort2))",
                                                                   "im(S(FloquetPort1,FloquetPort2))"]
                                             ], [])

    def setFrequencySweep(self, minFreq, maxFreq, rangeCount):
        self.minFrequency = minFreq
        self.maxFrequency = maxFreq
        self.setFrequencySolution(maxFreq)
        self.oModuleAnalysisSetup.EditFrequencySweep(Hfss.ANALYSIS_SETUP_NAME, Hfss.SWEEP_NAME,
                                                     [
                                                         "NAME:" + Hfss.SWEEP_NAME,
                                                         "IsEnabled:=", True,
                                                         "RangeType:=", "LinearCount",
                                                         "RangeStart:=", str(minFreq) + "GHz",
                                                         "RangeEnd:=", str(maxFreq) + "GHz",
                                                         "RangeCount:=", rangeCount,
                                                         "Type:=", "Interpolating",
                                                         "SaveFields:=", False,
                                                         "SaveRadFields:=", False,
                                                         "InterpTolerance:=", 0.5,
                                                         "InterpMaxSolns:=", 250,
                                                         "InterpMinSolns:=", 0,
                                                         "InterpMinSubranges:=", 1,
                                                         "ExtrapToDC:=", False,
                                                         "InterpUseS:=", True,
                                                         "InterpUsePortImped:=", False,
                                                         "InterpUsePropConst:=", True,
                                                         "UseDerivativeConvergence:=", False,
                                                         "InterpDerivTolerance:=", 0.2,
                                                         "UseFullBasis:=", True,
                                                         "EnforcePassivity:=", True,
                                                         "PassivityErrorTolerance:=", 0.0001
                                                     ])

    def setFrequencySolution(self, frequency):
        self.oModuleAnalysisSetup.EditSetup(Hfss.ANALYSIS_SETUP_NAME,
                                            [
                                                "NAME:" + Hfss.ANALYSIS_SETUP_NAME,
                                                "AdaptMultipleFreqs:=", False,
                                                "Frequency:=", str(frequency) + "GHz",
                                                "MaxDeltaS:=", 0.005,
                                                "PortsOnly:=", False,
                                                "UseMatrixConv:=", False,
                                                "MaximumPasses:=", 25,
                                                "MinimumPasses:=", 2,
                                                "MinimumConvergedPasses:=", 2,
                                                "PercentRefinement:=", 30,
                                                "IsEnabled:=", True,
                                                "BasisOrder:=", 1,
                                                "DoLambdaRefine:=", True,
                                                "DoMaterialLambda:=", True,
                                                "SetLambdaTarget:=", False,
                                                "Target:=", 0.3333,
                                                "UseMaxTetIncrease:=", False,
                                                "PortAccuracy:=", 2,
                                                "UseABCOnPort:=", False,
                                                "SetPortMinMaxTri:=", False,
                                                "UseDomains:=", False,
                                                "UseIterativeSolver:=", False,
                                                "SaveRadFieldsOnly:=", False,
                                                "SaveAnyFields:=", True,
                                                "IESolverType:=", "Auto",
                                                "LambdaTargetForIESolver:=", 0.15,
                                                "UseDefaultLambdaTgtForIESolver:=", True
                                            ])

    def setTheta(self, theta):
        self.theta = theta
        self.oModuleOptimetrics.EditSetup(Hfss.OPTEMETRIC_SETUP_NAME,
                                          [
                                              "NAME:" + Hfss.OPTEMETRIC_SETUP_NAME,
                                              "IsEnabled:=", True,
                                              [
                                                  "NAME:ProdOptiSetupDataV2",
                                                  "SaveFields:=", False,
                                                  "CopyMesh:=", False,
                                                  "SolveWithCopiedMeshOnly:=", True
                                              ],
                                              [
                                                  "NAME:StartingPoint"
                                              ],
                                              "Sim. Setups:=", [Hfss.ANALYSIS_SETUP_NAME],
                                              [
                                                  "NAME:Sweeps",
                                                  [
                                                      "NAME:SweepDefinition",
                                                      "Variable:=", "$theta_scan",
                                                      "Data:=", str(theta) + "deg",
                                                      "OffsetF1:=", False,
                                                      "Synchronize:=", 0
                                                  ]
                                              ],
                                              [
                                                  "NAME:Sweep Operations"
                                              ],
                                              [
                                                  "NAME:Goals"
                                              ]
                                          ])

    def analyzeData(self):
        self.oDesign.Analyze(Hfss.ANALYSIS_SETUP_NAME + " : " + Hfss.SWEEP_NAME)
        self.oModuleReportSetup.ExportToFile(Hfss.REPORT_NAME,
                                             self.outputFolder + "/Sparam_" + str(self.theta) + "_" + str
                                             (self.minFrequency) + "to" + str(self.maxFrequency) + ".csv")

    def terminate(self):
        self.oModuleAnalysisSetup.DeleteSetups([Hfss.ANALYSIS_SETUP_NAME])
        self.oModuleOptimetrics.DeleteSetups([Hfss.OPTEMETRIC_SETUP_NAME])
