import visualizations.utilization_factor_histograms as utilization_factor_histograms
import visualizations.mean_number_queue_histograms as mean_number_queue_histograms
import visualizations.response_time_histograms as response_time_histograms
import visualizations.sim_model_utilization_factor_histograms as sim_model_utilization_factor_histograms
import visualizations.sim_model_utilization_factor_cat_histograms as sim_model_utilization_factor_cat_histograms
import visualizations.sim_model_response_time_histograms as sim_model_response_time_histograms
import visualizations.sim_model_response_timeB_histograms as sim_model_response_timeB_histograms
import visualizations.sim_model_arrival_rate_histograms as sim_model_arrival_rate_histograms
import visualizations.sim_model_service_demand_histograms as sim_model_service_demand_histograms
import visualizations.sim_model_N_vs_U as sim_model_N_vs_U

import visualizations.convergence as convergence


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

scenarios = ["2-4-8-16/"]

seed_list = ["1996", "2006"]
policy_list = ["FIFO", "RR"]
preemption_list = ["preempt_no", "preempt_yes"]


sim_time_end_list = [5000, 50000, 400000, 500000]


path_to_print_pre = "../model_charts/"

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
    
    mean_number_queue_histograms.plot(files_list, policies, path_to_print)
    
    sim_model_utilization_factor_histograms.plot(files_list, policies, path_to_print)
    
    sim_model_N_vs_U.plot(files_list, policies, path_to_print)
    
    response_time_histograms.plot(files_list, policies, path_to_print)
    
    print("Metà")
    
    sim_model_response_time_histograms.plot(files_list, policies, path_to_print)
    
    sim_model_response_timeB_histograms.plot(files_list, policies, path_to_print)
    
    sim_model_arrival_rate_histograms.plot(files_list, policies, path_to_print)
    
    sim_model_service_demand_histograms.plot(files_list, policies, path_to_print)
    
    sim_model_utilization_factor_cat_histograms.plot(files_list, policies, path_to_print)
    
    ##################################
    #PREPARATION SECOND CHART
    ##############################

    scenarios = ["2-4-8-16_convergence/"]

    files_list = []
    for sim_time_end in sim_time_end_list:
        scenario = scenarios[0]
        preemption = preemption_list[0]
        seed = seed_list[0]
        policy = policy_list[0]

        path_to_print = path_to_print_pre + scenarios[0]
        
        f_name = build_name_function(path_to_tests, scenario, seed, policy, preemption, sim_time_end)
        files_list.append(f_name)

    convergence.plot(files_list, sim_time_end_list, path_to_print)





