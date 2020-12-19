import jmespath 
import json


def compute_total_cost(path):
    file_json = open(path, "r")
    json_data = json.load(file_json)
    
    list_result = jmespath.search("[*].cost", json_data)

    return sum(list_result)


