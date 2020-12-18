# Test
In this folder you can find all the oldest tests done with the simulator. Since we associate an id to each test, the Tests id section will do the association for each test id to the property of the test and the scope behind its execution. Furthermore the simulator used and its mode will be written.

# Repository composition
In the tests folder the user can find a folder for each test id.

Each of these will contain the pdf of the results and an internals folder composed of:
- `LP.txt`: Association LP-element used in the run.
- `topology.txt`: The topology parsed to run the simulation.
- `tests_topology`: A folder containing both the config.txt to let the generator create the topology and the catalog of the types used in the topology.

# Tests id

- `test01`: Done 17/11/2020, used to check correctness of simulator when scaling the number of local nodes per regional node while mantaining the original rates and properties. Done with ROOT-Sim, sequential execution. It is composed by one regional with 2 local nodes, one with 4, one with 8 and one with 16. Each local node has 1 LAN with 5 telemetry sensors, 1 transition sensor, 1 actuator. As expected the utilization factor of the regional scales linearly up until almost saturation.

- `test01`: Done 17/11/2020, similar to the previous test done as a first version of how load balancing could turn out(without actual implementation). Done with ROOT-Sim, sequential execution. It is composed by one regional with 2 local nodes, 7 regionals with 4 local nodes. Each local node has 1 LAN with 5 telemetry sensors, 1 transition sensor, 1 actuator.

- `test scheduler algorithms`: Test done to understand the effect of different scheduling policies on the model parameters.

- `test_new_formula`: Test done to compare the RB formula to the simulator computed response time.

- `compare_reply_no_reply`: test done to compare the effect of replies on the model

# Warning
The internals are different from the one used to run the test and may encounter errors when trying to use the configuration on the updated version of the simulator. At least some work to restructure the topology is expected.
