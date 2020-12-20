import visualizations.utilization_factor_histograms as utilization_factor_histograms

############################
#UTILS
##############################
def build_name_function(path_to_tests, scenario, seed, policy, preemption):
    name = "target_all-"
    name += "seed_" + str(seed) + "-"
    name += "timeout_none-rootsim-serial-threads_0-"
    name += policy + "-"
    name += preemption + "-"
    name += "sim_proc_no-lp_aggr_regional/" #aggr_central
    return path_to_tests + scenario + name


###################################
#PATH DATA
##################################

path_to_tests = "../model_tests/"

scenarios = ["2-4-8-16/"]

seed_list = ["1996", "2006"]
policy_list = ["FIFO", "RR"]
preemption_list = ["preempt_yes", "preempt_no"]


path_to_print = "../model_charts/"

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
            f_name = build_name_function(path_to_tests, scenarios[0], seed, policy, preemption)
            files_list[index].append(f_name)
        
        policies.append( (policy, preemption) )

        index += 1

print(policies)
#plot charts
utilization_factor_histograms.plot(files_list, policies, path_to_print)



##################################
#PREPARATION SECOND CHART
##############################





