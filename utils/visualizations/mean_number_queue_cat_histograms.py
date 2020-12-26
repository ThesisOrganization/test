from plot_functions.plot_graph import *
from data_extraction.take_groups import get_type_groups, select_simulation_groups_dict, create_dicts, divide_types

import json
import jmespath
import numpy as np
import os



def group_node_computation(groups, type_element):
    return_list_total_U = []
    list_names = []
    number = 0
    for group in groups:
        tel = np.array(jmespath.search("[*].parameters.telemetry.number_mean_queue", group))
        tra = np.array(jmespath.search("[*].parameters.transition.number_mean_queue", group))
        com = np.array(jmespath.search("[*].parameters.command.number_mean_queue", group))
        bat = np.array(jmespath.search("[*].parameters.batch.number_mean_queue", group))

        tel_mean = np.mean(tel)
        tra_mean = np.mean(tra)
        com_mean = np.mean(com)
        bat_mean = np.mean(bat)
        total = [tel_mean, tra_mean, com_mean, bat_mean]

        return_list_total_U.append(total)
        list_names.append(type_element + " type " + str(number))
        number += 1

    #print(return_list_total_U)

    return return_list_total_U, list_names

def group_lan_computation(groups, type_element):
    return_list_total_U = []
    list_names = []
    number = 0
    for group in groups:
        tel = np.array(jmespath.search("[*].lan_in.telemetry.number_mean_queue", group))
        tra = np.array(jmespath.search("[*].lan_in.transition.number_mean_queue", group))
        com = np.array(jmespath.search("[*].lan_in.command.number_mean_queue", group))
        bat = np.array(jmespath.search("[*].lan_in.batch.number_mean_queue", group))

        #total = [tel, tra, com, bat]
        #mean = np.mean(total)
        tel_mean = np.mean(tel)
        tra_mean = np.mean(tra)
        com_mean = np.mean(com)
        bat_mean = np.mean(bat)
        total = [tel_mean, tra_mean, com_mean, bat_mean]

        return_list_total_U.append(total)
        list_names.append(type_element + "_in type " + str(number))
        
        tel = np.array(jmespath.search("[*].lan_out.telemetry.number_mean_queue", group))
        tra = np.array(jmespath.search("[*].lan_out.transition.number_mean_queue", group))
        com = np.array(jmespath.search("[*].lan_out.command.number_mean_queue", group))
        bat = np.array(jmespath.search("[*].lan_out.batch.number_mean_queue", group))

        tel_mean = np.mean(tel)
        tra_mean = np.mean(tra)
        com_mean = np.mean(com)
        bat_mean = np.mean(bat)
        total = [tel_mean, tra_mean, com_mean, bat_mean]

        return_list_total_U.append(total)
        list_names.append(type_element + "_out type " + str(number))
        number += 1

    return return_list_total_U, list_names


def plot(files_list, name_files, path_out):
    index_file = 0

    directory_name = "mean_number_queue_cat_histograms/"
    if not os.path.exists(path_out + directory_name):
        os.makedirs(path_out + directory_name)

    list_data_to_plot = []

    for list_policy_files in files_list:
        results_value_seeds = []
        names = None
        for path_file in list_policy_files:
            file_name = "model_res.json"
            file_json = open(path_file + file_name, "r")
            json_data = json.load(file_json)
            file_json.close()

            file_name = "simulation_results.json"
            file_json = open(path_file + file_name, "r")
            sim_data = json.load(file_json)
            file_json.close()

            total_list_U = []
            names = []

            central_list, regionals_list, local_list, lan_list, actuator_list = divide_types(json_data)
            central_dict, regionals_dict, local_dict, lan_dict, actuator_dict = create_dicts(sim_data)


            central_group = get_type_groups(central_list)
            sim_central_group = select_simulation_groups_dict(central_group, central_dict)
            U_central, name = group_node_computation(sim_central_group, "central")
            total_list_U += U_central
            names += name
            #print(U_central)

            regional_group = get_type_groups(regionals_list)
            sim_regional_group = select_simulation_groups_dict(regional_group, regionals_dict)
            U_regionals, name = group_node_computation(sim_regional_group, "regional")
            total_list_U += U_regionals
            names += name
            #print(U_regionals)

            local_group = get_type_groups(local_list)
            sim_local_group = select_simulation_groups_dict(local_group, local_dict)
            U_locals, name = group_node_computation(sim_local_group, "local")
            total_list_U += U_locals
            names += name
            #print(U_locals)

            actuator_group = get_type_groups(actuator_list)
            sim_actuator_group = select_simulation_groups_dict(actuator_group, actuator_dict)
            U_actuactor, name = group_node_computation(sim_actuator_group, "actuator")
            total_list_U += U_actuactor
            names += name
            #print(U_actuactor)

            lan_group = get_type_groups(lan_list)
            sim_lan_group = select_simulation_groups_dict(lan_group, lan_dict)
            U_lan, name = group_lan_computation(sim_lan_group, "lan")
            total_list_U += U_lan
            names += name
            #print(U_lan)

            results_value_seeds.append(total_list_U)

        array_np = np.array(results_value_seeds)
        final_result = np.mean(array_np, axis=0)

        #draw_histograms(list(final_result), names, "Utilization factor", "Element Type", "U", 0.0, np.amax(final_result))

        max_value = np.amax(final_result)
        PERCENTAGE = 0.1
        list_data_to_plot.append((np.transpose(final_result), names, "Mean number of jobs", "Element Type", "N", 0.0, max_value + max_value*PERCENTAGE, ["Telemetry", "Transition", "Command", "Batch"], path_out + directory_name + name_files[index_file][0] + "_" + name_files[index_file][1]))


        index_file += 1
    
    max_value = 0
    for data in list_data_to_plot:
        if max_value < data[6]:
            max_value = data[6]


    for data in list_data_to_plot:
        p0, p1, p2, p3, p4, p5, p6, p7, p8 = data
        draw_grouped_histograms(p0, p1, p2, p3, p4, p5, max_value, p7, PATH=p8)

        


            
