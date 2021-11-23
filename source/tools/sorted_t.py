"""
Tools PampaMT
Author: Patrick Rogger Garcia
Date: 2018/09/01


Sort the bt_plots according to the periods
"""

def sorted_t(list_bt_plot):

    dict_sorted = {}

    status = False
    for bt_plot in list_bt_plot:

        if str(bt_plot.obj_file.T[bt_plot.n - 1]) in dict_sorted.keys():
            status = True
            break

        dict_sorted[str(bt_plot.obj_file.T[bt_plot.n - 1])] = bt_plot

    list_int_x = []
    for key in dict_sorted.keys():
        list_int_x.append(float(key))

    sorted_list_dict_keys = sorted(list_int_x)

    list_sorted_bt_plot = []
    for T in sorted_list_dict_keys:
        list_sorted_bt_plot.append(dict_sorted[str(T)])

    return status, list_sorted_bt_plot, bt_plot