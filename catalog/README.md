# Catalog

This folder represents the catalog and will contain a folder for each type of element. Inside these folder there will be all the types of that element.

# Types

Now we will briefly present the available types for the element and the general rule to name them.

To name a type and be consistend with several element we use the following string: "`Type-[name of the type of test / criteria of the type characteristic]-[progressive number]`".
The `progressive-number` file is used to identify several types of the same element with an id (starting from 0) that match the same test type or criteria.

In some cases the name of the type will contain the `magnitude_[number]` substring. This indicates that the type is a variation of another type, which shares the same base name, and the values have been rescaled by multiplying them by 10^[number].

Finally, the sensor types will have `telemetry` or `transition` is their name to identify if they are telemetry or transition sensors.

# Available Types

- `Type-test_80_400`: The types used during the test 80-400, which was the first test that stressed out the model, it used a balanced tree with:
	- 80 regional nodes
	- 5 local node per regional node
	- 1 lan per local node
	- 1 actuator per lan
	- 1 transition sensor per lan
	- 5 telemetry sensor per lan

- `Type-realistic_magnitude_1`: Types used with a realistic (but fake) scale between the parameters of the different classes.
