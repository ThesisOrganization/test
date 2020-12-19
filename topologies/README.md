# Performance Tests

This folder will contain all the topologies used in the tests.

# Topologies

- `80-400`: A simple balanced tree composed of elements of type `Type-test_80_400-0` with:
	- 80 regional nodes
	- 5 local node per regional node
	- 1 lan per local node
	- 1 actuator per lan
	- 1 transition sensor per lan
	- 5 telemetry sensor per lan

- `8-40`: A smaller variation of the `80-400`.

- `8-40-realistic`: A variation of `8-40` which uses the type `Type-realistic_magnitude_1-0` for its elements.

- `80-400-realistic`: A variation of `80-400` which uses the type `Type-realistic_magnitude_1-0` for its element.

- `2-4-8-16`: An unbalanced tree with elements of typer `Type-realistic_magnitude_1-0`, which is composed by:
	- 1 regional node with 2 local nodes
	- 1 regional node with 4 local nodes
	- 1 regional node with 8 local nodes
	- 1 regional node with 16 local nodes
	- 1 lan per local node
	- 1 actuator per lan
	- 1 transition sensor per lan
	- 5 telemetry sensor per lan