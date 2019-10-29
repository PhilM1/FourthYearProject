class Design:

    def __init__(self):
        self.val = 0

    def GetModule(self, module_name):
        print("     self.o_design.GetModule(" + module_name + ")")
        if module_name == "AnalysisSetup":
            return AnalysisSetup()
        if module_name == "Optimetrics":
            return Optimetrics()
        if module_name == "ReportSetup":
            return ReportSetup()

    def Analyze(self, analysis_name):
        print("     self.o_design.Analyze(" + analysis_name + ")")

    def ChangeProperty(self, input):
        print("     self.o_design.ChangeProperty(" + str(input) + ")")


class AnalysisSetup:

    def __init__(self):
        self.val = 0

    def InsertSetup(self, name, input):
        print("     self.module_analysis_setup.InsertSetup(" + name + "," + str(input) + ")")

    def InsertFrequencySweep(self, name, input):
        print("     self.module_analysis_setup.InsertFrequencySweep(" + name + "," + str(input) + ")")

    def EditFrequencySweep(self, name, name2, input):
        print("     self.module_analysis_setup.EditFrequencySweep(" + name + "," + name2 + "," + str(input) + ")")

    def EditSetup(self, name, input):
        print("     self.module_analysis_setup.EditSetup(" + name + "," + str(input) + ")")

    def DeleteSetups(self, input):
        print("     self.module_analysis_setup.DeleteSetups(" + str(input) + ")")


class Optimetrics:

    def __init__(self):
        self.val = 0

    def InsertSetup(self, name, input):
        print("     self.module_optimetrics.InsertSetup(" + name + "," + str(input) + ")")

    def EditSetup(self, name, input):
        print("     self.module_optimetrics.EditSetup(" + name + "," + str(input) + ")")

    def DeleteSetups(self, input):
        print("     self.module_optimetrics.DeleteSetups(" + str(input) + ")")


class ReportSetup:

    def CreateReport(self, a, b, c, d, e, f, g, h):
        print("     self.module_report_setup.CreateReport(" + str(a) + "," + str(b) + "," + str(c) + "," + str(d) + "," + str(
            e) + "," + str(f) + "," + str(g) + "," + str(h) + ")")

    def ExportToFile(self, reportName, outputFile):
        print("     self.module_report_setup.ExportToFile(" + reportName + "," + outputFile + "," + str(input) + ")")