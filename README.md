# Test
In this repo you can find all the tests done with the simulator. Since we associate an id to each test, the Tests id section will do the association for each test id to the property of the test and the scope behind its execution. Furthermore the simulator used and its mode will be written.

# Repository composition

- `catalog`: A unique catalog for all the updated tests, contains the types of all elements.

- `topologies`: This folder will contain all the topologies used for the tests.

- `legacy_tests`: The oldest test in done with the simulator, many of them are not up to date with the simulator interals. Refeter to the readme in that folder for more info.

- `performance tests`: Tests done to evaluate the model performance with several simulator configurations. They all use the global catalog.

- `model_tests`: Tests done to compare the analytical and simulation model.

- `utils`: several utility scripts.