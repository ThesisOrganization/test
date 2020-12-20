import jmespath 
import json


def compute_total_cost(json_data):
    
    list_result = jmespath.search("[*].cost", json_data)

    return sum(list_result)


