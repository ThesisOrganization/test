# Test
In this repo you can find all the tests done with the simulator. Since we associate an id to each test, the Tests id section will do the association for each test id to the property of the test and the scope behind its execution. Furthermore the simulator used and its mode will be written.

# Repository composition
In the tests folder the user can find a folder for each test id.\
Each of these will containt the pdf of the results and an internals folder composed of:\
- `LP.txt`: Association LP-element used in the run.\
- `topology.txt`: The topology parsed to run the simulation.\
- `tests_topology`: A folder containing both the config.txt to let the generator create the topology and the catalog of the types used in the topology.

# Tests id

- `test01`: Done 17/11/2020, used to check correctness of simulator when scaling the number of local nodes per regional node while mantaining the original rates and properties. Done with ROOT-Sim, sequential execution. In total 4 regional nodes, 30 local nodes. Each local node having 5 telemetry sensors, 1 transition sensor, 1 actuator.

