from plot_functions.plot_graph import *
from data_extraction.take_groups import get_type_groups, select_simulation_groups_dict, create_dicts, divide_types

import json
import jmespath
import numpy as np
import os



def get_parameters_lan(sim_data, data_before):
    tel_out_sim = np.array(jmespath.search("[*].lan_out.telemetry.number_mean_queue", sim_data))
    tra_out_sim = np.array(jmespath.search("[*].lan_out.transition.number_mean_queue", sim_data))
    com_out_sim = np.array(jmespath.search("[*].lan_out.command.number_mean_queue", sim_data))
    bat_out_sim = np.array(jmespath.search("[*].lan_out.batch.number_mean_queue", sim_data))
    
    tel_out_sim = tel_out_sim[tel_out_sim>0.0]
    tra_out_sim = tra_out_sim[tra_out_sim>0.0]
    com_out_sim = com_out_sim[com_out_sim>0.0]
    bat_out_sim = bat_out_sim[bat_out_sim>0.0]

    tel_out_before = np.array(jmespath.search("[*].lan_out.telemetry.number_mean_queue", data_before))
    tra_out_before = np.array(jmespath.search("[*].lan_out.transition.number_mean_queue", data_before))
    com_out_before = np.array(jmespath.search("[*].lan_out.command.number_mean_queue", data_before))
    bat_out_before = np.array(jmespath.search("[*].lan_out.batch.number_mean_queue", data_before))

    tel_out_before = tel_out_before[tel_out_before>0.0]
    tra_out_before = tra_out_before[tra_out_before>0.0]
    com_out_before = com_out_before[com_out_before>0.0]
    bat_out_before = bat_out_before[bat_out_before>0.0]

    tel_out_diff = np.absolute( tel_out_sim - tel_out_before )
    tel_out_max = np.maximum(tel_out_sim, tel_out_before)
    tel_out_division = np.nan_to_num(tel_out_diff / tel_out_max)

    tra_out_diff = np.absolute( tra_out_sim - tra_out_before )
    tra_out_max = np.maximum(tra_out_sim, tra_out_before)
    tra_out_division = np.nan_to_num(tra_out_diff / tra_out_max)

    com_out_diff = np.absolute( com_out_sim - com_out_before )
    com_out_max = np.maximum(com_out_sim, com_out_before)
    com_out_division = np.nan_to_num(com_out_diff / com_out_max)

    bat_out_diff = np.absolute( bat_out_sim - bat_out_before )
    bat_out_max = np.maximum(bat_out_sim, bat_out_before)
    bat_out_division = np.nan_to_num(bat_out_diff / bat_out_max)

    tel_out_mean = np.mean(tel_out_division)
    if np.isnan(tel_out_mean):
        tel_out_mean = []
    else:
        tel_out_mean = [tel_out_mean]
    tra_out_mean = np.mean(tra_out_division)
    if np.isnan(tra_out_mean):
        tra_out_mean = []
    else:
        tra_out_mean = [tra_out_mean]
    com_out_mean = np.mean(com_out_division)
    if np.isnan(com_out_mean):
        com_out_mean = []
    else:
        com_out_mean = [com_out_mean]
    bat_out_mean = np.mean(bat_out_division)
    if np.isnan(bat_out_mean):
        bat_out_mean = []
    else:
        bat_out_mean = [bat_out_mean]

    mean_list_final = []
    mean_list_final += tel_out_mean
    mean_list_final += tra_out_mean
    mean_list_final += com_out_mean
    mean_list_final += bat_out_mean

    out_mean = np.mean(np.array(mean_list_final))


    tel_in_sim = np.array(jmespath.search("[*].lan_in.telemetry.number_mean_queue", sim_data))
    tra_in_sim = np.array(jmespath.search("[*].lan_in.transition.number_mean_queue", sim_data))
    com_in_sim = np.array(jmespath.search("[*].lan_in.command.number_mean_queue", sim_data))
    bat_in_sim = np.array(jmespath.search("[*].lan_in.batch.number_mean_queue", sim_data))

    tel_in_sim = tel_in_sim[tel_in_sim>0.0]
    tra_in_sim = tra_in_sim[tra_in_sim>0.0]
    com_in_sim = com_in_sim[com_in_sim>0.0]
    bat_in_sim = bat_in_sim[bat_in_sim>0.0]

    tel_in_before = np.array(jmespath.search("[*].lan_in.telemetry.number_mean_queue", data_before))
    tra_in_before = np.array(jmespath.search("[*].lan_in.transition.number_mean_queue", data_before))
    com_in_before = np.array(jmespath.search("[*].lan_in.command.number_mean_queue", data_before))
    bat_in_before = np.array(jmespath.search("[*].lan_in.batch.number_mean_queue", data_before))

    tel_in_before = tel_in_before[tel_in_before>0.0]
    tra_in_before = tra_in_before[tra_in_before>0.0]
    com_in_before = com_in_before[com_in_before>0.0]
    bat_in_before = bat_in_before[bat_in_before>0.0]

    tel_in_diff = np.absolute( tel_in_sim - tel_in_before )
    tel_in_max = np.maximum(tel_in_sim, tel_in_before)
    tel_in_division = np.nan_to_num(tel_in_diff / tel_in_max)

    tra_in_diff = np.absolute( tra_in_sim - tra_in_before )
    tra_in_max = np.maximum(tra_in_sim, tra_in_before)
    tra_in_division = np.nan_to_num(tra_in_diff / tra_in_max)

    com_in_diff = np.absolute( com_in_sim - com_in_before )
    com_in_max = np.maximum(com_in_sim, com_in_before)
    com_in_division = np.nan_to_num(com_in_diff / com_in_max)

    bat_in_diff = np.absolute( bat_in_sim - bat_in_before )
    bat_in_max = np.maximum(bat_in_sim, bat_in_before)
    bat_in_division = np.nan_to_num(bat_in_diff / bat_in_max)

    tel_in_mean = np.mean(tel_in_division)
    if np.isnan(tel_in_mean):
        tel_in_mean = []
    else:
        tel_in_mean = [tel_in_mean]
    tra_in_mean = np.mean(tra_in_division)
    if np.isnan(tra_in_mean):
        tra_in_mean = []
    else:
        tra_in_mean = [tra_in_mean]
    com_in_mean = np.mean(com_in_division)
    if np.isnan(com_in_mean):
        com_in_mean = []
    else:
        com_in_mean = [com_in_mean]
    bat_in_mean = np.mean(bat_in_division)
    if np.isnan(bat_in_mean):
        bat_in_mean = []
    else:
        bat_in_mean = [bat_in_mean]


    mean_list_final = []
    mean_list_final += tel_in_mean
    mean_list_final += tra_in_mean
    mean_list_final += com_in_mean
    mean_list_final += bat_in_mean

    in_mean = np.mean(np.array(mean_list_final))

    mean_list_final_again = []
    mean_list_final_again += [out_mean]
    mean_list_final_again += [in_mean]


    return [np.mean(np.array(mean_list_final_again))]

def get_parameters(sim_data, data_before):
    tel_sim = np.array(jmespath.search("[*].parameters.telemetry.number_mean_queue", sim_data))
    tra_sim = np.array(jmespath.search("[*].parameters.transition.number_mean_queue", sim_data))
    com_sim = np.array(jmespath.search("[*].parameters.command.number_mean_queue", sim_data))
    bat_sim = np.array(jmespath.search("[*].parameters.batch.number_mean_queue", sim_data))


    tel_sim = tel_sim[tel_sim>0.0]
    tra_sim = tra_sim[tra_sim>0.0]
    com_sim = com_sim[com_sim>0.0]
    bat_sim = bat_sim[bat_sim>0.0]

    tel_before = np.array(jmespath.search("[*].parameters.telemetry.number_mean_queue", data_before))
    tra_before = np.array(jmespath.search("[*].parameters.transition.number_mean_queue", data_before))
    com_before = np.array(jmespath.search("[*].parameters.command.number_mean_queue", data_before))
    bat_before = np.array(jmespath.search("[*].parameters.batch.number_mean_queue", data_before))

    tel_before = tel_before[tel_before>0.0]
    tra_before = tra_before[tra_before>0.0]
    com_before = com_before[com_before>0.0]
    bat_before = bat_before[bat_before>0.0]

    tel_diff = np.absolute( tel_sim - tel_before )
    tel_max = np.maximum(tel_sim, tel_before)
    tel_division = np.nan_to_num(tel_diff / tel_max)

    tra_diff = np.absolute( tra_sim - tra_before )
    tra_max = np.maximum(tra_sim, tra_before)
    tra_division = np.nan_to_num(tra_diff / tra_max)

    com_diff = np.absolute( com_sim - com_before )
    com_max = np.maximum(com_sim, com_before)
    com_division = np.nan_to_num(com_diff / com_max)

    bat_diff = np.absolute( bat_sim - bat_before )
    bat_max = np.maximum(bat_sim, bat_before)
    bat_division = np.nan_to_num(bat_diff / bat_max)

    tel_mean = np.mean(tel_division)
    tra_mean = np.mean(tra_division)
    com_mean = np.mean(com_division)
    bat_mean = np.mean(bat_division)

    tel_mean = np.mean(tel_division)
    if np.isnan(tel_mean):
        tel_mean = []
    else:
        tel_mean = [tel_mean]
    tra_mean = np.mean(tra_division)
    if np.isnan(tra_mean):
        tra_mean = []
    else:
        tra_mean = [tra_mean]
    com_mean = np.mean(com_division)
    if np.isnan(com_mean):
        com_mean = []
    else:
        com_mean = [com_mean]
    bat_mean = np.mean(bat_division)
    if np.isnan(bat_mean):
        bat_mean = []
    else:
        bat_mean = [bat_mean]

    mean_list_final = []
    mean_list_final += tel_mean
    mean_list_final += tra_mean
    mean_list_final += com_mean
    mean_list_final += bat_mean

    mean = np.mean(np.array(mean_list_final))

    return [mean]


def difference(sim_data, data_before):

    central_list, regionals_list, local_list, lan_list, actuator_list = divide_types(sim_data)
    central_before_list, regionals_before_list, local_before_list, lan_before_list, actuator_before_list = divide_types(data_before)
    
    mean_list = []

    mean_list += get_parameters(central_list + regionals_list + local_list + actuator_list, central_before_list + regionals_before_list + local_before_list + actuator_before_list)
    mean_list += get_parameters_lan(lan_list, lan_before_list)
    
    mean = np.mean(np.array(mean_list))

    return mean



def plot(files_list, sim_time_end_list, path_out):
    index_file = 0

    directory_name = "convergence/"
    if not os.path.exists(path_out + directory_name):
        os.makedirs(path_out + directory_name)

    
    files_list_without_first = files_list[1:]
    file_name = "simulation_results.json"

    path_file = files_list[0]
    file_json = open(path_file + file_name, "r")
    sim_data = json.load(file_json)
    file_json.close()

    data_before = sim_data

    mean_list = []
    
    for path_file in files_list_without_first:
        file_json = open(path_file + file_name, "r")
        sim_data = json.load(file_json)
        file_json.close()

        mean = difference(sim_data, data_before)
        mean_list.append(mean)

        data_before = sim_data

    #print(mean_list)
    
    draw_lines(mean_list, list(map(str, sim_time_end_list[1:])), "Convergence", "Simulation time", "Diff", 0.0, 0.3, PATH=path_out + directory_name + "convergence")

            
