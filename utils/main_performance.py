import os
from plot_functions import plot_graph
import re
import math
import json
from response_time_computation.total_response_time import compute_total_response_time

def get_data(path_to_tests,scenarios,simulator_list,threads_list,sim_proc_list,lp_aggr_list,preempt_list,parameters_list):
	data_dict={}
	test_folder_list=[]
	for elem in os.listdir(path_to_tests):
		if elem[0] != ".":
			scenarios_path=os.path.join(path_to_tests,elem)
			if "optimized" == elem or "no_central" == elem:
				scenario_dirs=[]
				for dir in os.listdir(scenarios_path):
					scenario_dirs.append(os.path.join(scenarios_path,dir))
			else:
				scenario_dirs=[scenarios_path]
			for dir in scenario_dirs:
				for scenario in scenarios:
					if scenario in dir and "old" not in dir:
						chosen_scenario=scenario
						test_folder_list.append(dir)
	for path in test_folder_list:
		dirlist=os.listdir(path=path)

		for dir in dirlist:
			parameters_got=0
			tmp_dict=data_dict
			simulator=""
			n_threads=-1
			conf=chosen_scenario+"-"
			#choosing the nested dictionary that complies with the test configuration (specified in the directory name)
			for sim in simulator_list:
				if sim in dir:
					simulator=sim
					parameters_got+=1
			for preempt in preempt_list:
				if "preempt_"+preempt in dir:
					conf+="preempt_"+preempt+"-"
					parameters_got+=1
			for sim_proc in sim_proc_list:
				if "sim_proc_"+sim_proc in dir:
					conf+= "sim_proc_"+sim_proc+"-"
					parameters_got+=1
			for lp_aggr in lp_aggr_list:
				if "lp_aggr_"+lp_aggr in dir:
					conf+="lp_aggr_"+lp_aggr
					parameters_got+=1
			if "parallel" in dir:
				for threads in threads_list:
					if "threads_"+str(threads)+"-" in dir:
						n_threads=threads
						parameters_got+=1
			elif "serial" in dir and 0 in threads_list:
				n_threads=1
				parameters_got+=1
			elif "optimized" in path:
				parameters_got+=1
				res=re.match('.*threads_([0-9]+)-.*',dir)
				n_threads=int(res.groups()[0])
				if n_threads==0:
					n_threads=1

			if parameters_got >= 5:
				sequential_run=False
				if simulator == "use":
					sim="USE"
					f_path=os.path.join(path,dir+"/USE_output.txt")
					try:
							os.stat(f_path)
					except IOError:
						print(f"{f_path} unavailable, skipping")
						continue

				elif simulator == "rootsim":
					f_path=os.path.join(path,dir+"/outputs/execution_stats")
					try:
						os.stat(f_path)
					except IOError:
						f_path=os.path.join(path,dir+"/outputs/sequential_stats")
						sequential_run=True
						try:
							os.stat(f_path)
						except IOError:
							print(f"both {path}/outputs/execution_stats and {path}/outputs/sequential_stats unavailable, skipping")
							continue

					sim="ROOT-Sim"

				if "optimized" in f_path:
					sim="Optimized "+sim
				elif "no_central" in f_path:
					sim=sim+" no central"


				try:
					if os.stat(f_path).st_size == 0:
						print(f"{f_path} empty, skipping")
					else:
						if tmp_dict.get(conf) == None:
							tmp_dict.update( {conf : {} })
						tmp_dict=tmp_dict.get(conf)

						if tmp_dict.get(sim) == None:
							tmp_dict.update({ sim: {} })
						tmp_dict=tmp_dict.get(sim)

						for param in parameters_list:
							if tmp_dict.get(param) == None:
								tmp_dict.update({param:{}})
						stats_f=open(f_path)
						lines=stats_f.readlines()
						if simulator == "use":
							for line in lines:
								if "Starting an execution with " in line:
									sequential_run=int(line.strip().split(" ")[4])==1
								if "Rollback operations................................................:" in line:
									tmp_dict.get(parameters_list[0]).update({n_threads : int(line.strip().split(" ")[-1])})
								if "AVG Rollbacked Events per Rollback.................................:" in line:
									if sequential_run:
										tmp_dict.get(parameters_list[1]).update({n_threads : 0})
									else:
										tmp_dict.get(parameters_list[1]).update({n_threads : round(float(line.strip().split(" ")[-1]),3)})
								if "Total allocated space...........................:" in line:
									split_line=line.strip().split(" ")
									if split_line[-1]=="GB":
										multiplier=1024
									elif split_line[-1]=="MB":
										multiplier=1
									elif split_line[-1]=="KB":
										multiplier=0.001024
									tmp_dict.get(parameters_list[2]).update({n_threads : round(float(split_line[-2])*multiplier,3)})
								if "EventsPerSec:" in line:
									tmp_dict.get(parameters_list[3]).update({n_threads : round(float(line.strip().split(" ")[-1]),3)})
						if simulator == "rootsim":
							if sequential_run:
								tmp_dict.get(parameters_list[0]).update({n_threads : 0})
								tmp_dict.get(parameters_list[1]).update({n_threads : 0})
								line=lines[16].strip().split(" ")
								if line[-1]=="GB":
									multiplier=1024
								elif line[-1]=="MB":
									multiplier=1
								elif line[-1]=="KB":
									multiplier=0.001024
								tmp_dict.get(parameters_list[2]).update({n_threads : round(float(lines[16].strip().split(" ")[-2])*multiplier) })
								tmp_dict.get(parameters_list[3]).update({n_threads : int(lines[9].strip().split(" ")[-1])/float(lines[6].strip().split(" ")[-2]) })
							else:
								tmp_dict.get(parameters_list[0]).update({n_threads : int(lines[33].strip().split(" ")[-1])})
								tmp_dict.get(parameters_list[1]).update({n_threads : round(float(lines[36].strip().split(" ")[-2]),3)})
								line=lines[49].strip().split(" ")
								if line[-1]=="GB":
									multiplier=1024
								elif line[-1]=="MB":
									multiplier=1
								elif line[-1]=="KB":
									multiplier=0.001024
								tmp_dict.get(parameters_list[2]).update({n_threads : round(float(line[-2])*multiplier,3) })
								tmp_dict.get(parameters_list[3]).update({n_threads : round(int(lines[31].strip().split(" ")[-1])/float(lines[23].strip().split(" ")[-2]),3) })
				except IOError:
					print(f"File {f_path} not accessible, skipped")
				finally:
					if os.stat(f_path).st_size != 0:
						stats_f.close()

	for conf in data_dict.keys():
		conf_dict=data_dict[conf]
		data_dict.update({conf : dict(sorted(conf_dict.items(),key=lambda kv: 1 if kv[0] == 'ROOT-Sim' else 3 if kv[0] == 'Optimized ROOT-Sim' else 2 if kv[0] == 'USE' else 4 ))})
	return data_dict


def plot_opt_comparison(data_dict,parameters_list,scenario_list,preempt_list,thread_list,sim_proc_list,lp_aggr_list,simulator_list,folder):
	markers_list=[8,10,9,11]
	colors_list=['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628']
	for param in parameters_list:
		grouped_data=[]
		data_min=-1
		data_max=-1
		for preempt in preempt_list:
			for sim_proc in sim_proc_list:
				for lp_aggr in lp_aggr_list:
					for scenario in scenario_list:
						for conf in data_dict.keys():
							if scenario+"-preempt_"+preempt+"-sim_proc_"+sim_proc+"-lp_aggr_"+lp_aggr in conf:
								legend=[]
								for sim in simulator_list:
									legend.append(sim)
									tmp_dict=data_dict[conf][sim][param]
									data=[]
									for thread in thread_list:
										value=tmp_dict.get(thread)
										if value!=None and (data_min==-1 or value<data_min):
											data_min=value
										if value!=None and (data_max==-1 or value>data_max):
											data_max=value
										data.append(value)
									grouped_data.append(data)
								plot_graph.draw_grouped_lines(grouped_data, range(len(thread_list)), "","Threads", param,colors=colors_list[0:len(grouped_data)],markers=markers_list[0:len(legend)],legend=legend,x_tick_labels=thread_list,PATH=os.path.join(folder,param))

def plot_central_no_central_comparison(data_dict,parameters_list,scenario_list,preempt_list,thread_list,sim_proc_list,lp_aggr_list,simulator_list,folder):
	colors_list=['#a6cee3','#1f78b4','#b2df8a','#33a02c']
	hatches_list=['','x','|','\\','/','+','x','o','.','-']
	conf_string=""
	for param in parameters_list:
		sims=[]
		data=[]
		confs=[]
		for sim in simulator_list:
			if sim not in sims:
				sims.append(sim)
			for preempt in preempt_list:
				for sim_proc in sim_proc_list:
					for lp_aggr in lp_aggr_list:
						for thread in thread_list:
							for scenario in scenario_list:
								for conf in data_dict.keys():
									if scenario+"-preempt_"+preempt+"-sim_proc_"+sim_proc+"-lp_aggr_"+lp_aggr in conf:
										confs.append(conf)
										conf_string=conf
										data.append(data_dict[conf][sim][param].get(thread))
		plot_graph.draw_histograms(data,sims,"","",param,PATH=os.path.join(folder,param),COLOR=colors_list[:len(data)])

def plot_conf_comparison(data_dict,parameters_list,scenario_list,preempt_list,thread_list,sim_proc_list,lp_aggr_list,simulator_list,fname,varying_param,folder):

	data=[]
	markers_list=[8,10,9,11]
	hatches_list=['','+','-','|','\\','/','.','x','.',]
	colors_list=['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628']
	for param in parameters_list:
		sims=[]
		data_by_sim=[]
		for i in range(0,len(simulator_list)):
			data_by_sim.append([])
		grouped_data=[]
		for preempt in preempt_list:
			for sim_proc in sim_proc_list:
				for lp_aggr in lp_aggr_list:
					for thread in thread_list:
						for scenario in scenario_list:
							for i in range(0,len(simulator_list)):
								for conf in data_dict.keys():
									if fname=="combo" and preempt != sim_proc:
										break
									if scenario+"-preempt_"+preempt+"-sim_proc_"+sim_proc+"-lp_aggr_"+lp_aggr in conf:
										data=[]
										if simulator_list[i] not in sims:
											sims.append(simulator_list[i])
										#if len(thread_list) == 1 and len(lp_aggr_list)==1:
										#	data.append(data_dict[conf][simulator_list[i]][param].get(thread))
										#else:
										data_by_sim[i].append(data_dict[conf][simulator_list[i]][param].get(thread))
									if len(data)!=0:
										grouped_data.append(data)
		if len(thread_list) == 1 and len(lp_aggr_list)==1:
			plot_graph.draw_grouped_histograms(data_by_sim,varying_param,"","",param,legend_labels=sims,PATH=os.path.join(folder,param),colors=colors_list[:len(data_by_sim)],hatches=hatches_list[:len(data_by_sim)])
		else:
			if len(thread_list)==1:
				names=lp_aggr_list
				label="Entity to LP mapping"
			else:
				label="Threads"
				names=thread_list
			plot_graph.draw_grouped_lines(data_by_sim, range(len(names)), "",label, param,colors=colors_list[0:len(data_by_sim)],PATH=os.path.join(folder,param),markers=markers_list[:len(data_by_sim)],x_tick_labels=names,legend=sims)



path_to_tests = "../performance_tests"
charts_path="../performance_charts"
scenarios = ["80-400"]

timeout_list = ["300"]
simulator_list = ["rootsim", "use"]
threads_list = [0,2,5,10,20,30,40]
sim_proc_list = ["no", "yes"]
lp_aggr_list = ["regional", "local", "lan"]
preempt_list = ["no","yes"]
parameters_list=["Number of executed rollback operations","Average rollback length","Allocated memory (MB)","Number of processed events per second"]

data_dict=get_data(path_to_tests,scenarios,simulator_list,threads_list,sim_proc_list,lp_aggr_list,preempt_list,parameters_list)

plot_opt_comparison(data_dict,parameters_list,["80-400"],["no"],[1,2,5,10,20,30,40],["yes"],["regional"],["ROOT-Sim", "USE", "Optimized ROOT-Sim", "Optimized USE"],charts_path+"/opt")

plot_conf_comparison(data_dict,parameters_list,["80-400"],["no","yes"],[5],["no"],["regional"],["ROOT-Sim", "USE"],"preempt_no_yes",["no preemption","preemption"],charts_path+"/preemption")

plot_conf_comparison(data_dict,parameters_list,["80-400"],["no"],[5],["no","yes"],["regional"],["ROOT-Sim", "USE"],"sim_proc_no_yes",["no sim_proc","sim_proc"],charts_path+"/sim_proc")

plot_conf_comparison(data_dict,parameters_list,["80-400"],["no","yes"],[5],["no","yes"],["regional"],["ROOT-Sim", "USE"],"combo",["no preemption + no sim_proc","preemption + sim_proc"],charts_path+"/combo")

plot_conf_comparison(data_dict,parameters_list,["80-400"],["no"],[5],["no"],["regional","local","lan"],["ROOT-Sim", "USE"],"lp_aggr_regional_local_lan",["regional mapping","local mapping","lan mapping"],charts_path+"/lp_aggr")

plot_conf_comparison(data_dict,parameters_list,["80-400"],["no"],[1,2,5,10,20,30,40],["no"],["regional"],["ROOT-Sim", "USE"],"threads_1_2_5_10_20_30_40",[1,2,5,10,20,30,40],charts_path+"/threads")

plot_central_no_central_comparison(data_dict,parameters_list,scenarios,["no"],[5],["no"],["regional"],["ROOT-Sim","ROOT-Sim no central"],charts_path+"/no_central")

for usecase0dir in os.listdir("../use_cases/UseCase0"):
	usecase0_f=open("../use_cases/UseCase0/"+usecase0dir+"/simulation_results.json","r")
	usecase0_json=json.load(usecase0_f)
	usecase0_f.close()
	usecase0_data=compute_total_response_time(usecase0_json,0)
	usecase0_res_f=open("../use_cases/UseCase0/"+usecase0dir+"/total_response_times.json","w")

	usecase0_res_dict={}
	message_classes=["telemetry","transition","command","batch"]
	for message_class in range(0,len(message_classes)) :
		usecase0_res_dict.update({ message_classes[message_class] : usecase0_data[message_class]})
		print(f"{message_classes[message_class]} response time: {usecase0_data[message_class]} ")
	json.dump(usecase0_res_dict,usecase0_res_f,indent=2)
	usecase0_res_f.close()

