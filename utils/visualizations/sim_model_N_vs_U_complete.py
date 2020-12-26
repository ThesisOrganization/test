from plot_functions.plot_graph import *
from data_extraction.take_groups import get_type_groups, select_simulation_groups_dict, create_dicts, divide_types

import json
import jmespath
import numpy as np
import os



def plot(files_list, name_files, path_out):
    index_file = 0

    directory_name = "sim_model_N_over_U_complete/"
    if not os.path.exists(path_out + directory_name):
        os.makedirs(path_out + directory_name)

    list_data_to_plot = []

    for list_policy_files in files_list:
        results_value_seeds = []
        results_x_value = []
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

            sim_data = jmespath.search("[?type!='wan']", sim_data)
            
            model_data_sorted = sorted(json_data, key=lambda x: x["id"])
            sim_data_sorted = sorted(sim_data, key=lambda x: x["id"])
            
            len_data = len(sim_data_sorted)
            if len_data != len(model_data_sorted):
                print("len_data != len(model_data_sorted)")
                return
            
            U_list = []
            data_list = []
            for i in range(0, len_data):
                model_element = model_data_sorted[i]
                sim_element = sim_data_sorted[i]

                if sim_element["type"] != "lan":
                    value_sim = np.array(jmespath.search("parameters.*.number_mean_queue", sim_element))
                    value_model = np.array(jmespath.search("parameters.*.number_mean_queue", model_element))
                    diff = np.absolute(value_sim - value_model)

                    #max_b = np.maximum(value_model, value_sim)
                    division = np.nan_to_num(diff / value_model)
                    #division = np.nan_to_num(diff / max_b)

                    #data_list.append(np.mean(division))
                    data_list.append(division)
                    
                    u_sim = np.array(jmespath.search("parameters.*.utilization_factor", sim_element))
                    u_tot = np.sum(u_sim)
                    u_array = np.empty(4)
                    u_array.fill(u_tot)
                    U_list.append(u_array)


                else:
                    value_sim = np.array(jmespath.search("*.*.number_mean_queue", sim_element))
                    value_model = np.array(jmespath.search("*.*.number_mean_queue", model_element))
                    diff = np.absolute(value_sim - value_model)
                    
                    #max_b = np.maximum(value_model, value_sim)
                    division = np.nan_to_num(diff / value_model)
                    #division = np.nan_to_num(diff / max_b)

                    #data_list.append(np.mean(division[0]))
                    #data_list.append(np.mean(division[1]))
                    data_list.append(division[0])
                    data_list.append(division[1])
                    
                    u_sim = np.array(jmespath.search("*.*.utilization_factor", sim_element))
                    u_tot = np.sum(u_sim[0])
                    u_array = np.empty(4)
                    u_array.fill(u_tot)
                    U_list.append(u_array)

                    u_tot = np.sum(u_sim[1])
                    u_array = np.empty(4)
                    u_array.fill(u_tot)
                    U_list.append(u_array)




            #m_n = np.array(jmespath.search("[*].*.*.number_mean_queue", model_data_sorted))
            #s_n = np.array(jmespath.search("[*].*.*.number_mean_queue", sim_data_sorted))

            #s_u = np.array(jmespath.search("[*].*.*.utilization_factor", sim_data_sorted))

            #function = np.vectorize(mapping)

            #diff = np.absolute(m_n - s_n)
            #division = diff / m_n

            #final_result = np.flatten(division)
            final_result = np.transpose(data_list)
            #final_result = data_list
            final_result_x = np.transpose(U_list)
            #final_result_x = U_list

        max_value = np.amax(final_result)
        PERCENTAGE = 0.1

        #list_data_to_plot.append((list(final_result), list(final_result_x), [], "Scatterplot utilization factor and difference in percentage for N between model and simulation", "U", "Diff(N_m - N_s)", 0.0, max_value + PERCENTAGE*max_value, path_out + directory_name + name_files[index_file][0] + "_" + name_files[index_file][1]))
        list_data_to_plot.append((list(final_result), list(final_result_x), ["Telemetry", "Transition", "Command", "Batch"], "Scatterplot utilization factor and difference in percentage for N between model and simulation", "U", "Diff(N_m - N_s)", 0.0, max_value + PERCENTAGE*max_value, path_out + directory_name + name_files[index_file][0] + "_" + name_files[index_file][1]))


        index_file += 1
    
    max_value = 0
    for data in list_data_to_plot:
        if max_value < data[7]:
            max_value = data[7]


    for data in list_data_to_plot:
        p0, p1, p2, p3, p4, p5, p6, p7, p8 = data
        #draw_scatterplot(p0, p1, p2, p3, p4, p5, p6, max_value, PATH=p8)
        draw_classes_scatterplot(p0, p1, p2, p3, p4, p5, p6, max_value, PATH=p8)

        


            
