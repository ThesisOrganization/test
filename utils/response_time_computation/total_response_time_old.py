import json

import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)


class Container:
    def __init__(self):
        self.data = None
        self.sons = []

def setup_dict(json_data):
    dict_global = {}

    for node in json_data:
        id_node = node["id"]

        if id_node not in dict_global:
            dict_global[id_node] = Container()
        
        dict_global[id_node].data = node

        next_id = dict_global[id_node].data["upper_node"]


        if next_id not in dict_global:
            dict_global[next_id] = Container()

        dict_global[next_id].sons.append(dict_global[id_node])

    return dict_global


#######################
#UTILS
###################

def get_max(l1, l2):
    m1 = max(l1[0], l2[0])
    m2 = max(l1[1], l2[1])
    m3 = max(l1[2], l2[2])
    m4 = max(l1[3], l2[3])
    return (m1, m2, m3, m4)

def sum_tuple(l1, l2):
    return (l1[0] + l2[0], l1[1] + l2[1], l1[2] + l2[2], l1[3] + l2[3])


####################
#response time 
##################

RESPONSE_TYPE = 0 #0->all, 1->regional + local, 2->local


def compute_response(container):
    
    #################################
    #taking my response times
    ######################à
    if container.data["type"] == "wan":
        delay = container.data["delay"]
        my_response = (delay, delay, delay, delay)
    elif container.data["type"] == "lan":
        telemetry_response = container.data["lan_out"]["telemetry"]["response_time"]
        transition_response = container.data["lan_out"]["transition"]["response_time"]
        command_response = container.data["lan_in"]["command"]["response_time"]
        batch_response = container.data["lan_out"]["batch"]["response_time"]

        my_response = (telemetry_response, transition_response, command_response, batch_response)
    else:
        telemetry_response = container.data["parameters"]["telemetry"]["response_time"]
        transition_response = container.data["parameters"]["transition"]["response_time"]
        command_response = container.data["parameters"]["command"]["response_time"]
        batch_response = container.data["parameters"]["batch"]["response_time"]

        my_response = (telemetry_response, transition_response, command_response, batch_response)

    ##################################
    #calling all my sons
    #############################
    max_response = (0.0, 0.0, 0.0, 0.0)
    for son in container.sons:
        ret_response = compute_response(son)
        max_response = get_max(max_response, ret_response)
    

    ############################
    #returning values based on who I am
    ############################
    if RESPONSE_TYPE == 0:
        return sum_tuple(max_response, my_response)
    if RESPONSE_TYPE == 1:
        if container.data["type"] == "node" and container.data["node_type"] == "central":
            return max_response
        else:
            return sum_tuple(max_response, my_response)
    if RESPONSE_TYPE == 2:
        if container.data["type"] == "node" and (container.data["node_type"] == "central" or container.data["node_type"] == "regional"):
            return max_response
        else:
            return sum_tuple(max_response, my_response)


#path = "../tests_topology/tests/rootsim-serial-threads_0-FIFO-preempt_no-sim_proc_no-seed_-1-timeout_none/simulation_results.json"
path = "./simulation_results.json"


file_json = open(path, "r")

json_data = json.load(file_json)

dict_global = setup_dict(json_data)



print(compute_response(dict_global[0]))


