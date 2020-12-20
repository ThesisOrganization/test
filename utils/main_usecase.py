import visualizations.utilization_factor_histograms as utilization_factor_histograms


def build_name_function(path_to_tests, scenario, seed, policy, preemption):
    name = "target_all-"
    name += "seed_" + str(seed) + "-"
    name += "timeout_none-rootsim-serial-threads_0-"
    name += policy + "-"
    name += preemption + "-"
    name += "sim_proc_no-lp_aggr_central/"
    return path_to_tests + scenario + name


path_to_tests = "../model_tests/"

scenarios = ["2-4-8-16/"]

seed_list = ["1996", "2006"]
policy_list = ["FIFO", "RR"]
preemption_list = ["preempt_yes", "preempt_no"]
