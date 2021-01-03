import visualizations.utilization_factor_histograms as utilization_factor_histograms
import visualizations.utilization_factor_cat_histograms as utilization_factor_cat_histograms
import visualizations.mean_number_queue_histograms as mean_number_queue_histograms
import visualizations.mean_number_queue_cat_histograms as mean_number_queue_cat_histograms
import visualizations.response_time_histograms as response_time_histograms
import visualizations.arrival_rate_histograms as arrival_rate_histograms

import visualizations.sim_model_utilization_factor_histograms as sim_model_utilization_factor_histograms
import visualizations.sim_model_utilization_factor_cat_histograms as sim_model_utilization_factor_cat_histograms
import visualizations.sim_model_response_time_histograms as sim_model_response_time_histograms
import visualizations.sim_model_N_cat_histograms as sim_model_N_cat_histograms
import visualizations.sim_model_response_timeB_histograms as sim_model_response_timeB_histograms
import visualizations.sim_model_arrival_rate_histograms as sim_model_arrival_rate_histograms
import visualizations.sim_model_service_demand_histograms as sim_model_service_demand_histograms
import visualizations.sim_model_N_vs_U as sim_model_N_vs_U
import visualizations.sim_model_N_vs_U_complete as sim_model_N_vs_U_complete
import visualizations.sim_model_N_vs_U_sum as sim_model_N_vs_U_sum
import visualizations.sim_model_R_vs_U_complete as sim_model_R_vs_U_complete

import visualizations.convergence as convergence

import visualizations.cost_performance as cost_performance
from response_time_computation.total_response_time import compute_total_response_time
from cost_computation.total_cost import compute_total_cost

############################
#UTILS
##############################
def build_name_function(path_to_tests, scenario, seed, policy, preemption, sim_time_end=None):
    name = "target_all-"
    name += "seed_" + str(seed) + "-"
    name += "timeout_none-rootsim-serial-threads_0-"
    name += policy + "-"
    name += preemption + "-"
    name += "sim_proc_no-lp_aggr_central" #aggr_central
    if sim_time_end != None:
        name += "-sim_time_end_" + str(sim_time_end)
    name += "/"
    return path_to_tests + scenario + name


###################################
#PATH DATA
##################################

path_to_tests = "../model_tests/"

#scenarios = ["2-4-8-16/"]

MAX_VALUE_YES = True

#############
#FINAL TESTS
############
scenarios = ["usecase1/", "usecase2/"]  #REALISTIC

max_values = [3.0, 3.0]  #REALISTIC
if MAX_VALUE_YES:
    max_values = [None, None]  #REALISTIC



seed_list = ["1996"]
#seed_list = ["1492"]

#############
#FINAL TESTS
############

policy_list = ["FIFO"]
preemption_list = ["preempt_no"]



path_to_print_pre = "../model_charts/"
max_index_used = 0

for scenario in scenarios:
    
    path_to_print = path_to_print_pre + scenario
    
    ##################################
    #PREPARATION FIRST CHART
    ##############################
    
    files_list = []
    policies = []
    index = 0
    for policy in policy_list:
        for preemption in preemption_list:
            files_list.append([])
    
            for seed in seed_list:
                f_name = build_name_function(path_to_tests, scenario, seed, policy, preemption)
                files_list[index].append(f_name)
            
            policies.append( (policy, preemption) )
    
            index += 1
    
    #plot charts

    utilization_factor_histograms.plot(files_list, policies, path_to_print)
    
    utilization_factor_cat_histograms.plot(files_list, policies, path_to_print)
    
    mean_number_queue_histograms.plot(files_list, policies, path_to_print)
    
    mean_number_queue_cat_histograms.plot(files_list, policies, path_to_print)
    
    response_time_histograms.plot(files_list, policies, path_to_print)

    arrival_rate_histograms.plot(files_list, policies, path_to_print)
    
    print("Sim model Comparison")

    sim_model_utilization_factor_histograms.plot(files_list, policies, path_to_print, passed_max_value=max_values[max_index_used])

    ##DISABLED
    ##sim_model_N_vs_U.plot(files_list, policies, path_to_print)

    sim_model_N_vs_U_complete.plot(files_list, policies, path_to_print)
    
    sim_model_N_vs_U_sum.plot(files_list, policies, path_to_print)
    
    sim_model_R_vs_U_complete.plot(files_list, policies, path_to_print)
    
    sim_model_response_time_histograms.plot(files_list, policies, path_to_print, passed_max_value=max_values[max_index_used])
    
    sim_model_N_cat_histograms.plot(files_list, policies, path_to_print, passed_max_value=max_values[max_index_used])
    
    sim_model_response_timeB_histograms.plot(files_list, policies, path_to_print, passed_max_value=max_values[max_index_used])
    
    sim_model_arrival_rate_histograms.plot(files_list, policies, path_to_print, passed_max_value=max_values[max_index_used])
    
    sim_model_service_demand_histograms.plot(files_list, policies, path_to_print, passed_max_value=max_values[max_index_used])
    
    sim_model_utilization_factor_cat_histograms.plot(files_list, policies, path_to_print, passed_max_value=max_values[max_index_used])

    max_index_used += 1
    

print("Cost and performance")

names_scenarios = ["Normal", "Modified"]


for policy in policy_list:
    for preemption in preemption_list:
        files_list = []
        for scenario in scenarios:
            #preemption = preemption_list[0]
            seed = seed_list[0]
            #policy = policy_list[0]
        
            f_name = build_name_function(path_to_tests, scenario, seed, policy, preemption)
            
            files_list.append(f_name)
        
        cost_performance.plot(files_list, path_to_print_pre + "cost_performance/" + policy + "_" + preemption + "/", compute_total_response_time, compute_total_cost, names_scenarios)


