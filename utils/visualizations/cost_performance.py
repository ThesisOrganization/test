from plot_functions.plot_graph import *

import json
import jmespath
import numpy as np
import os


def plot(files_list, path_out, compute_total_response_time, compute_total_cost, name_scenarios):

    directory_name = "cost_performance/"
    if not os.path.exists(path_out + directory_name):
        os.makedirs(path_out + directory_name)
    
    file_name = "simulation_results.json"

    cost_list = []
    response_time_list = []
    
    for path_file in files_list:
        file_json = open(path_file + file_name, "r")
        sim_data = json.load(file_json)
        file_json.close()

        response_time = compute_total_response_time(sim_data, 0)
        response_time1 = compute_total_response_time(sim_data, 1)
        response_time2 = compute_total_response_time(sim_data, 2)
        
        r2 = np.array(response_time2)
        r1 = np.array(response_time1)
        r0 = np.array(response_time)

        #print(r0 - r2)

        #response_time_list.append(response_time)
        response_time_list.append(list(r0 - r2))

        cost = compute_total_cost(sim_data)
        cost_list.append(cost)

    
    classes = ["Telemetry", "Transition", "Command", "Batch"]
    max_value = np.amax(np.array(response_time_list))
    PERCENTAGE = 0.15
    response_time_transpose = list(np.transpose(np.array(response_time_list)))
    draw_grouped_histograms(response_time_transpose, name_scenarios, "Total response time", "Class", "Response time", 0.0, max_value + max_value*PERCENTAGE, classes, PATH=path_out + directory_name + "Total_response_time")

    max_value = np.amax(np.array(cost_list))
    PERCENTAGE = 0.15
    draw_histograms(cost_list, name_scenarios, "Cost scenarios", "Scenario", "Costs", 0.0, max_value + max_value*PERCENTAGE, ISSCIE=False, PATH=path_out + directory_name + "Total_costs")

