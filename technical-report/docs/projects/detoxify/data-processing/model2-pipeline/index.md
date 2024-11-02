---
updated: 4 October 2024
authors:
  - Richmond Sin
---

# Data Pipeline

## [Kedro](https://docs.kedro.org/en/0.19.6/introduction/index.html)

Kedro is an open-source framework to create maintainable and modular data science pipelines. We are using kedro version `0.19.6` in our data pipelines. These pipelines are stored in the `content-optimization` directory.
You can refer to the [Get Started](https://docs.kedro.org/en/stable/get_started/index.html) guide for more information.

Before running or editing the Kedro pipeline, it is recommended to install the project in the `content-optimization` directory -

```python
# Install the Kedro Project
pip install -e .
```

This is important so that your Integrated Development Environment (IDE) can properly index the imports in your scripts.

## [Key Concepts](https://docs.kedro.org/en/0.19.6/get_started/kedro_concepts.html)

### [Nodes](https://docs.kedro.org/en/0.19.6/nodes_and_pipelines/nodes.html)

A node is a wrapper for a Python function to execute your data transformations. It is the building block of a pipeline. In your nodes, you should define your function used, name of inputs as well as outputs, and the name of your node.
You can refer to this [link](https://docs.kedro.org/en/0.19.6/nodes_and_pipelines/nodes.html) for more information.

### [Pipelines](https://docs.kedro.org/en/0.19.6/nodes_and_pipelines/pipeline_introduction.html)

A pipeline organises the dependencies and execution order of a collection of nodes and connects inputs and outputs while keeping your code modular. The pipeline determines the node execution order by resolving dependencies and does not necessarily run the nodes in the order in which they are passed in.
You can refer to this [link](https://docs.kedro.org/en/0.19.6/nodes_and_pipelines/pipeline_introduction.html) for more information.

### [Data Catalog](https://docs.kedro.org/en/0.19.6/data/index.html)

The Kedro Data Catalog is the registry of all data sources that the project can use to manage loading and saving data. It maps the names of node inputs and outputs as keys in a DataCatalog, a Kedro class that can be specialised for different types of data storage.
Kedro provides different built-in datasets for numerous file types and file systems, so you don’t have to write the logic for reading/writing data. You can refer to this [link](https://docs.kedro.org/en/0.19.6/data/index.html) for more information.

### [Parameters](https://docs.kedro.org/en/0.19.6/configuration/parameters.html)

Project parameters make your Kedro pipelines more flexible and easier to configure, since you can change the behaviour of your nodes. By default, in a new Kedro project, parameters are defined in the parameters.yml file, which is located in the project’s conf/base directory.
This file contains a dictionary of key-value pairs, where each key is a parameter name and each value is the corresponding parameter value. These parameters can serve as input to nodes and are used when running the pipeline.
You can refer to this [link](https://docs.kedro.org/en/0.19.6/configuration/parameters.html) for more information.

## [Datasets](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-4.1.0/)

`kedro-datasets` is a library that define all the available data connectors that can be integrated into the Kedro Pipeline. You would typically defined in the Data Catalog. You can refer to this [link](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-4.1.0/api/kedro_datasets.html) for the available data connectors.

## [Visualisations](https://docs.kedro.org/projects/kedro-viz/en/stable/)

Kedro-Viz is an interactive development tool for visualising data science pipelines built with Kedro. This is extremely useful for understanding how the data flows from node to node in your pipeline. You can refer to this [link](https://docs.kedro.org/projects/kedro-viz/en/stable/) for more information.

## [Tests](https://docs.kedro.org/en/stable/development/automated_testing.html)

Writing tests is extremely crucial to ensuring the robustness of your Kedro pipelines. You can setup automated testing using the `pytest` framework. You can refer to this [link](https://docs.kedro.org/en/stable/development/automated_testing.html#set-up-automated-testing-with-pytest) for more information.
