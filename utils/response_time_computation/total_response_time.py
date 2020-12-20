import json
import numpy as np

import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)


class Container:
    levels_to_add = 0 #0 -> all, 1-> regional + local, 2 -> local

    def compute_response(self):
        my_response = self.data

        max_response = np.array((0.0, 0.0, 0.0, 0.0))
        for son in self.sons:
            ret_response = son.compute_response()
            max_response = np.maximum(max_response, ret_response)

        if self.summable:
            return my_response + max_response
        else:
            return max_response


    def set_summable(self, summable):
        self.summable = summable
    
    def set_data(self, data):
        self.data = data

    def add_son(self, son):
        self.sons.append(son)

    def __init__(self):
        self.data = None
        self.sons = []


def get_data(node):
    if node["type"] == "wan":
        delay = node["delay"]
        my_response = (delay, delay, delay, delay)
    elif node["type"] == "lan":
        telemetry_response = node["lan_out"]["telemetry"]["response_time"]
        transition_response = node["lan_out"]["transition"]["response_time"]
        command_response = node["lan_in"]["command"]["response_time"]
        batch_response = node["lan_out"]["batch"]["response_time"]

        my_response = (telemetry_response, transition_response, command_response, batch_response)
    else:
        telemetry_response = node["parameters"]["telemetry"]["response_time"]
        transition_response = node["parameters"]["transition"]["response_time"]
        command_response = node["parameters"]["command"]["response_time"]
        batch_response = node["parameters"]["batch"]["response_time"]

        my_response = (telemetry_response, transition_response, command_response, batch_response)

    return np.array(my_response)


def get_summable(node):
    if Container.levels_to_add == 1 and node["type"] == "wan" and node["upper_node"] == 0:
        return False
    elif Container.levels_to_add == 2 and node["type"] == "wan":
        return False

    if Container.levels_to_add == 1 and node["type"] == "node" and node["node_type"] == "central":
        return False
    elif Container.levels_to_add == 2 and node["type"] == "node" and (node["node_type"] == "central" or node["node_type"] == "regional"):
        return False

    return True


def setup_dict(json_data):
    dict_global = {}

    for node in json_data:
        id_node = node["id"]

        if id_node not in dict_global:
            dict_global[id_node] = Container()
            #dict_global[id_node].summable = get_summable(node)
        
        #dict_global[id_node].data = get_data(node)
        dict_global[id_node].set_data(get_data(node))
        dict_global[id_node].set_summable(get_summable(node))

        next_id = node["upper_node"]

        if next_id not in dict_global:
            dict_global[next_id] = Container()

        #dict_global[next_id].sons.append(dict_global[id_node])
        dict_global[next_id].add_son(dict_global[id_node])

    return dict_global


def compute_total_response_time(json_data, levels=0):
    
    Container.levels_to_add = levels

    dict_global = setup_dict(json_data)
    
    final_response_time = dict_global[0].compute_response()

    return list(final_response_time)


#path = "../tests_topology/tests/rootsim-serial-threads_0-FIFO-preempt_no-sim_proc_no-seed_-1-timeout_none/simulation_results.json"
#path = "./simulation_results.json"
#
#
#results = compute_total_response_time(path, 0)
#
#print(results)

