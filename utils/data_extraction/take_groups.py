import json
import jmespath 


def build_parameters(element):
    if element["type"] == "lan":
        return [element["lan_in"], element["lan_out"]]
    elif element["type"] == "actuator":
        return [element["parameters"]]
    else:
        return [element["parameters"], element["num_cores"]]


def get_type_groups(list_elements):
    return_groups = [ [list_elements[0]] ]

    list_elements_without_first = list_elements[1:]
    for element in list_elements_without_first:
        element_parameters = build_parameters(element)
        inserted = False
        for group_list in return_groups:
            group = group_list[0]
            group_parameters = build_parameters(group)
            if element_parameters == group_parameters:
                group_list.append(element)
                inserted = True
                break
        if not inserted:
            return_groups.append([element])

    return return_groups


#def select_simulation_groups(groups, simulation_data):
#    return_list = []
#    num_groups = len(groups)
#    for i in range(0, num_groups):
#        return_list.append([])
#        num_element_in_group = len(groups[i])
#        for j in range(0, num_element_in_group):
#            element = groups[i][j]
#            simulation_element = jmespath.search("[?id==`" + str(element["id"]) + "`]", simulation_data)
#            return_list[i].append(simulation_element[0])
#
#    return return_list

def select_simulation_groups_dict(groups, sim_dict):
    return_list = []
    num_groups = len(groups)
    for i in range(0, num_groups):
        return_list.append([])
        num_element_in_group = len(groups[i])
        for j in range(0, num_element_in_group):
            element = groups[i][j]
            simulation_element = sim_dict[element["id"]]
            #simulation_element = jmespath.search("[?id==`" + str(element["id"]) + "`]", simulation_data)
            return_list[i].append(simulation_element)

    return return_list

def create_dicts(sim_data):
    n_central = {}
    n_regionals = {}
    n_locals = {}
    n_lans = {}
    n_actuators = {}
    for element in sim_data:
        if element["type"] == "node" and element["node_type"] == "central":
            n_central[element["id"]] = element
        elif element["type"] == "node" and element["node_type"] == "regional":
            n_regionals[element["id"]] = element
        elif element["type"] == "node" and element["node_type"] == "local":
            n_locals[element["id"]] = element
        elif element["type"] == "lan":
            n_lans[element["id"]] = element
        elif element["type"] == "actuator":
            n_actuators[element["id"]] = element

    return n_central, n_regionals, n_locals, n_lans, n_actuators


def divide_types(json_data):
    n_central = []
    n_regionals = []
    n_locals = []
    n_lans = []
    n_actuators = []
    for element in json_data:
        if element["type"] == "node" and element["node_type"] == "central":
            n_central.append(element)
        elif element["type"] == "node" and element["node_type"] == "regional":
            n_regionals.append(element)
        elif element["type"] == "node" and element["node_type"] == "local":
            n_locals.append(element)
        elif element["type"] == "lan":
            n_lans.append(element)
        elif element["type"] == "actuator":
            n_actuators.append(element)

    return n_central, n_regionals, n_locals, n_lans, n_actuators


def get_groups(json_data):
    central_list = jmespath.search("[?(type == 'node' && node_type == 'central')]", json_data)
    central_group = get_type_groups(central_list)

    regionals_list = jmespath.search("[?(type == 'node' && node_type == 'regional')]", json_data)
    regional_group = get_type_groups(regionals_list)

    local_list = jmespath.search("[?(type == 'node' && node_type == 'local')]", json_data)
    local_group = get_type_groups(local_list)

    actuactor_list = jmespath.search("[?(type == 'actuator')]", json_data)
    actuator_group = get_type_groups(actuactor_list)

    lan_list = jmespath.search("[?(type == 'lan')]", json_data)
    lan_group = get_type_groups(lan_list)

    return central_group + regional_group + local_group + actuator_group + lan_group





#path = "../model_res.json"
#file_json = open(path, "r")
#json_data = json.load(file_json)
#
#elements = jmespath.search("[?(type == 'node' && node_type == 'regional')]", json_data)
#elements = jmespath.search("[?(type == 'actuator')]", json_data)
#elements = jmespath.search("[?(type == 'lan')]", json_data)
#list_all = get_type_groups(elements)
#
#
#
#path_sim = "../test_simulation_results.json"
#file_json_sim = open(path_sim, "r")
#simulation_data = json.load(file_json_sim)
#
#simulation_list = select_simulation_groups(list_all, simulation_data)
#
#print(len(simulation_list))
#
##print(list_all[0][0]["parameters"] == simulation_list[0][0]["parameters"])
#print(list_all[0][0]["lan_in"] == simulation_list[0][0]["lan_in"])
#print(list_all[0][0]["lan_out"] == simulation_list[0][0]["lan_out"])
#print(list_all[0][0]["id"] == simulation_list[0][0]["id"])
#
#
#print(list_all[0][0]["lan_in"])
#print(list_all[0][0]["lan_out"])
##print(list_all[0][0]["parameters"])
#print(simulation_list[0][0]["lan_in"])
#print(simulation_list[0][0]["lan_out"])
##print(simulation_list[0][0]["parameters"])


#print(get_groups(json_data, simulation_data))
#print(len(get_groups(json_data, simulation_data)))






#path = "../model_res.json"
#file_json = open(path, "r")
#json_data = json.load(file_json)
#
#path_sim = "../test_simulation_results.json"
#file_json_sim = open(path_sim, "r")
#simulation_data = json.load(file_json_sim)
#
#groups = get_groups(json_data)
#
#
#sim_groups = select_simulation_groups(groups, simulation_data)
#
#print(sim_groups)
#print(len(sim_groups))


            
            


