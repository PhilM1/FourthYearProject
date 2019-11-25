"""
The use of this file is to compile methods for different test types. This will make it easier to switch between
using different tests. Furthurmore, the creating of tests in this format will allow for them to be tested beforehand
"""

from Hfss import Hfss


def basic_test_puck(o_design):
    """
    Basic theta sweep for the puck
    :param o_design:
    """
    parameter_names = []
    parameter_units = []
    report_variables = ["Freq:=", ["All"], "a:=", ["Nominal"], "t_sub:=", ["Nominal"], "t_copper:=", ["Nominal"],
                        "CylinderZ:=", ["Nominal"], "Crad:=", ["Nominal"], "Padding:=", ["Nominal"], "tau:=",
                        ["Nominal"],
                        "$phi_scan:=", ["All"], "$theta_scan:=", ["All"]]
    output_folder = "C:\\Users\\denisshleifman\\Desktop\\4thYearProject\\results"
    test_object = Hfss(o_design, parameter_names, parameter_units, report_variables, output_folder)
    test_object.set_frequency_sweep(1, 1.5, 10)

    theta = [20, 40]
    for x in theta:
        test_object.set_angle(x, 0)
        test_object.analyze_data()

    test_object.terminate()


def geometry_puck(o_design):
    """
    Basic theta sweep for the puck
    :param o_design:
    """
    parameter_names = ["CylinderZ", "Crad"]
    parameter_units = ["mm", "mm"]
    report_variables = ["Freq:=", ["All"], "a:=", ["Nominal"], "t_sub:=", ["Nominal"], "t_copper:=", ["Nominal"],
                        "CylinderZ:=", ["Nominal"], "Crad:=", ["Nominal"], "Padding:=", ["Nominal"], "tau:=",
                        ["Nominal"],
                        "$phi_scan:=", ["All"], "$theta_scan:=", ["All"]]
    output_folder = "C:\\Users\\denisshleifman\\Desktop\\4thYearProject\\results"
    test_object = Hfss(o_design, parameter_names, parameter_units, report_variables, output_folder)
    test_object.set_frequency_sweep(1, 1.5, 10)

    theta = [20, 40]
    cylinder_z = [5, 6]
    crad = [2, 3]

    for x in cylinder_z:
        test_object.set_parameter_index(0, x)
        for y in crad:
            test_object.set_parameter_index(1, y)
            for z in theta:
                test_object.set_angle(z, 0)
                test_object.analyze_data()

    test_object.terminate()
