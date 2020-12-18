import json

path = "./simulation_results_with_wan.json"

file_json = open(path, "r")
json_data = json.load(file_json)


for element in json_data:
    if element["type"] == "lan":
        element["lan_out"]["telemetry"]["response_time"] = 1.0
        element["lan_out"]["transition"]["response_time"] = 1.0
        element["lan_in"]["command"]["response_time"] = 1.0
        element["lan_out"]["batch"]["response_time"] = 1.0
    elif element["type"] == "wan":
        pass
    else:
        element["parameters"]["telemetry"]["response_time"] = 1.0
        element["parameters"]["transition"]["response_time"] = 1.0
        element["parameters"]["command"]["response_time"] = 1.0
        element["parameters"]["batch"]["response_time"] = 1.0




out = "./robe.json"

fout = open(out, "w")
json.dump(json_data, fout)

fout.close()
