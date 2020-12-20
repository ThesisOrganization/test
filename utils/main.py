from plot_functions.plot_graph import *
from response_time_computation.total_response_time import compute_total_response_time
from cost_computation.total_cost import compute_total_cost
from data_extraction.take_groups import get_type_groups, select_simulation_groups

import json
import jmespath


colors = ["red", "green", "yellow", "black", "blue"]


draw_histograms([2, 4, 4], ["Ciao", "hello", "bye"], "Robe super", "dd", "no", 0, 5, "red", PATH="file1.png")

grouped_values = [[1, 3, 6], [2, 4, 4], [5, 5, 2], [9, 5, 2], [3, 2, 1]]
#draw_grouped_histograms(grouped_values, ["Ciao", "hello", "bye"], "Robe super", "dd", "no", 0, max_groupes(grouped_values) + 1, ["robe", "hihi", "random", "yotobi", "ilgatto"], colors)

draw_grouped_histograms(grouped_values, ["Ciao", "hello", "bye"], "Robe super", "dd", "no", 0, max_groupes(grouped_values) + 1, ["robe", "hihi", "random", "yotobi", "ilgatto"], PATH="file2.png")




exams = {"AN1":30, "FDI1":30, "GEO":24, "FIS":30, "TDP":31,
        "PES":27, "TDS":25, "AN2":24, "OOP":28, "TC":30,
        "SDC":26, "FDI2":30, "CA":28, "ADC":30, "EOA":18,
        "BDD":30, "PFP":31, "SO":31, "RDC":21, "RO":31, "ELE":26}

marks = list(exams.values())
names = list(exams.keys())

#draw_histograms(marks, names, "Marks of exams over time", "Exams", "Marks", 0, max(marks) + 1)

tot = 0
numExams = 0
mean = []
mean2 = []

for mark in marks:
    tot += mark
    numExams += 1
    mean.append(tot / numExams)
    mean2.append((tot - mark) / numExams)

draw_lines(mean, names, "Average of marks over time", "Exams", "Mean of marks", 0, max(mean) + 1, PATH="file3.png")
#draw_lines(mean, names, "Average of marks over time", "Exams", "Mean of marks", 0, max(mean) + 1, "#ff00ff", "#00ffff")
#draw_lines(mean, names, "Average of marks over time", "Exams", "Mean of marks", 0, max(mean) + 1, "#ff00ff")
#draw_lines(mean, names, "Average of marks over time", "Exams", "Mean of marks", 0, max(mean) + 1, COLOR_POINT="#ff00ff")

draw_grouped_lines([mean, mean2], names, "rofefe", "examns", "mean", 0, max(mean) + 1, ["yellow", "blue"], PATH="file4.png")

path = "./test_simulation_results.json"

file_json = open(path, "r")
json_data = json.load(file_json)

file_json.close()

response_time = compute_total_response_time(json_data, 0)

print(response_time)

cost = compute_total_cost(json_data)

print(cost)


draw_scatterplot([1.0, 2.0, 2.0], [4.9, 3.0, 2.0], ["ciao", "robe", "ah"], "saldkal", "patate", "robe", 0.0, 5.0)

path = "./model_res.json"
file_json = open(path, "r")
json_data = json.load(file_json)

elements = jmespath.search("[?(type == 'node' && node_type == 'regional')]", json_data)
list_all = get_type_groups(elements)

path_sim = "./test_simulation_results.json"
file_json_sim = open(path_sim, "r")
simulation_data = json.load(file_json_sim)

simulation_list = select_simulation_groups(list_all, simulation_data)

print(list_all[0][0]["parameters"] == simulation_list[0][0]["parameters"])
print(list_all[0][0]["id"] == simulation_list[0][0]["id"])
print(list_all[0][0]["parameters"])
print(simulation_list[0][0]["parameters"])
