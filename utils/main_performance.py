import os
from plot_functions import plot_graph
import re
import math

def get_data(path_to_tests,scenarios,simulator_list,threads_list,sim_proc_list,lp_aggr_list,preempt_list,parameters_list):
	data_dict={}
	test_folder_list=[]
	for elem in os.listdir(path_to_tests):
		if elem[0] != ".":
			scenarios_path=os.path.join(path_to_tests,elem)
			if "optimized" == elem:
				scenario_dirs=[]
				for dir in os.listdir(scenarios_path):
					scenario_dirs.append(os.path.join(scenarios_path,dir))
			else:
				scenario_dirs=[scenarios_path]
			for dir in scenario_dirs:
				for scenario in scenarios:
					if scenario in dir:
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
					stats_f.close()

	for conf in data_dict.keys():
		conf_dict=data_dict[conf]
		data_dict.update({conf : dict(sorted(conf_dict.items(),key=lambda kv: 1 if kv[0] == 'ROOT-Sim' else 3 if kv[0] == 'Optimized ROOT-Sim' else 2 if kv[0] == 'USE' else 4 ))})
	return data_dict


def plot_graphs(data_dict,parameters_list):
	markers_list=[8,10,9,11]
	colors_list=['#e66101','#5e3c99','#fdb863','#b2abd2']
	for conf in data_dict.keys():
		rootsim_opt=[]
		use_opt=[]

		for param in parameters_list:
			grouped_data=[]
			legend=[]
			data_min=-1
			data_max=-1
			thread_list=[]
			for sim in data_dict[conf].keys():
				if "Optimized" in sim:
					if "ROOT-Sim" in sim:
						rootsim_opt.append(list(data_dict[conf][sim][param].values())[0])
					if "USE" in sim:
						use_opt.append(list(data_dict[conf][sim][param].values())[0])
				for thread in data_dict[conf][sim][param].keys():
						if thread not in thread_list:
							thread_list.append(thread)
				thread_list.sort()
			for sim in data_dict[conf].keys():
				legend.append(sim)
				tmp_dict=data_dict[conf][sim][param]
				data=[]
				for thread in thread_list:
					value=tmp_dict.get(thread)
					if value == None:
						data.append(None)
					else:
						if data_min==-1 or value<data_min:
							data_min=value
						if data_max==-1 or value>data_max:
							data_max=value
						data.append(value)
				grouped_data.append(data)

			plot_graph.draw_grouped_lines(grouped_data, thread_list, "","Threads", param,colors=colors_list[0:len(grouped_data)],markers=markers_list[0:len(legend)],legend=legend,x_tick_labels=thread_list,PATH=charts_path+"/"+conf+" "+param)


path_to_tests = "../performance_tests"
charts_path="../performance_charts"
scenarios = ["80-400"]

timeout_list = ["300"]
simulator_list = ["rootsim","use"]
threads_list = [2,5,10,20,30,40]
sim_proc_list = ["no"] #["no", "yes"]
lp_aggr_list = ["regional"]#["regional","local"]
preempt_list = ["no"]
parameters_list=["Rollback operations","Rollback length","Allocated Memory (MB)","Events per second"]
data_dict=get_data(path_to_tests,scenarios,simulator_list,threads_list,sim_proc_list,lp_aggr_list,preempt_list,parameters_list)
plot_graphs(data_dict,parameters_list)
