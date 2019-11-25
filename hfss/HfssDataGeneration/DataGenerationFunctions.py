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
    parameter_names = ["$theta_scan"]
    parameter_units = ["deg"]
    all_parameter_names = ["a", "t_sub", "t_copper", "CylinderZ", "Crad", "Padding", "tau", "$phi_scan", "$theta_scan"]
    output_folder = "C:\\Users\\denisshleifman\\Desktop\\4thYearProject\\results"
    test_object = Hfss(o_design, parameter_names, parameter_units, all_parameter_names, output_folder)
    test_object.set_frequency_sweep(1, 1.5, 10)

    theta = [20, 40]
    for x in theta:
        test_object.set_parameter_index(0, x)
        test_object.analyze_data()

    test_object.terminate()


def geometry_puck_test(o_design):
    """
    Basic theta sweep for the puck
    :param o_design:
    """
    parameter_names = ["CylinderZ", "Crad", "$theta_scan"]
    parameter_units = ["mm", "mm", "deg"]
    all_parameter_names = ["a", "t_sub", "t_copper", "CylinderZ", "Crad", "Padding", "tau", "$phi_scan", "$theta_scan"]
    output_folder = "C:\\Users\\denisshleifman\\Desktop\\4thYearProject\\results"
    test_object = Hfss(o_design, parameter_names, parameter_units, all_parameter_names, output_folder)

    test_object.set_frequency_sweep(1, 1.5, 10)
    theta = [20, 40]
    cylinder_z = [5, 6]
    crad = [2, 3]

    for x in cylinder_z:
        test_object.set_parameter_index(0, x)
        for y in crad:
            test_object.set_parameter_index(1, y)
            for z in theta:
                test_object.set_parameter_index(2, z)
                test_object.analyze_data()

    test_object.terminate()


def geometry_puck_run(o_design):
    """
    Basic theta sweep for the puck
    :param o_design:
    """
    parameter_names = ["CylinderZ", "Crad", "$theta_scan"]
    parameter_units = ["mm", "mm", "deg"]
    all_parameter_names = ["a", "t_sub", "t_copper", "CylinderZ", "Crad", "Padding", "tau", "$phi_scan", "$theta_scan"]
    output_folder = "C:\\Users\\denisshleifman\\Desktop\\4thYearProject\\results"
    test_object = Hfss(o_design, parameter_names, parameter_units, all_parameter_names, output_folder)

    test_object.set_frequency_sweep(1, 15, 25000)

    for x in range(10):
        test_object.set_parameter_index(0, x + 1)
        for y in range(10):
            test_object.set_parameter_index(1, y + 1)
            for z in range(90):
                test_object.set_parameter_index(2, z + 1)
                test_object.analyze_data()

    test_object.terminate()
