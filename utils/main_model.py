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

scenarios = ["2-4-8-16/"]

#seed_list = ["1996", "2006"]
#seed_list = ["1492", "1789", "1984", "2006", "2077"]
seed_list = ["1996"]
policy_list = ["FIFO", "RR"]
preemption_list = ["preempt_no", "preempt_yes"]


sim_time_end_list = [3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000]


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

convergence.plot(files_list, sim_time_end_list, path_to_print, "response_time")
convergence.plot(files_list, sim_time_end_list, path_to_print, "number_mean_queue")
convergence.plot(files_list, sim_time_end_list, path_to_print, "utilization_factor")
convergence.plot(files_list, sim_time_end_list, path_to_print, "lambda_in")
convergence.plot(files_list, sim_time_end_list, path_to_print, "service_demand")


scenarios = ["2-4-8-16/", "2-4-8-16_balanced/", "2-4-8-16_multicore/", "2-4-8-16_powerfull/"]
names_scenarios = ["unbalanced", "balanced", "multicore", "powerfull"]


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



