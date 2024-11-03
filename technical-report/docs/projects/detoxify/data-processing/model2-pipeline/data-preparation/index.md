---
updated: 4 October 2024
authors:
  - Richmond Sin
---

# Data Processing

## Introduction

Our primary goal is to merge the articles across different content categories. This is to facilitate the use of this dataset for downstream applications e.g. Clustering or Retrieval Augmented Generation (RAG).

In this pipeline, we focus on the following:

1. Standardising the column names
2. Adding back the missing data
3. Extracting the Content Body from its Raw HTML
4. Performing its new category (IA) mappings
5. Merging all of these data into 1 dataframe

## Setting up the Project

1. Download the [`GenAI - Full Content Export.zip`](https://github.com/) file.
2. Extract all the Excel files and place them in the [`content-optimization/data/01_raw`](https://github.com/) directory of the Kedro pipeline.
3. Download the [`missing_contents.zip`](https://github.com/) file.
4. Extract and move the [`missing_contents`] directory to the [`content-optimization/data/01_raw`](https://github.com/) directory of the Kedro pipeline.
5. Refer to the [`README.md`](https://github.com/) to setup and run the Kedro Pipeline

!!! Note

    We are only interested in running the `data_processing` pipeline. To do so, run the following command after setting up the virtual environment and its dependecies -
    ```python
    cd content-optimization
    # Run the Data processing pipeline
    kedro run --pipeline=data_processing
    ```

## Adding new Kedro nodes

When adding new kedro nodes, it is important to understand the key processes that accompany it. You will usually add the filepath(s) to the Data Catalog, supplement the required parameters and write your functions.

### [`Data Catalog`](https://github.com/)

The Data Catalog is one of the most important files in the Kedro Pipeline. It indicates where your files are located in the project. Kedro handles the loading and saving of data on your behalf. You do not need to specify it in your nodes.

Here is an example of how to define it:

```yaml
# Variable Name/Dictionary Key
merged_data:
  # File Type - Refer to kedro-datasets (https://github.com/) for the appropriate data connector
  type: pandas.ParquetDataset
  # File Path - Indicate where to save/load the desired file
  filepath: data/03_primary/merged_data.parquet
  # Data Versioning - Indicate whether you want to only obtain the latest file or track the changes (via timestamp)
  versioned: true
```

Once you have defined your variables, you can use them in your Kedro pipeline.

### [`Parameters`](https://github.com/)

The Parameters are used to store any static definition of variables in the Kedro Pipeline. Each Pipeline has its own set of parameters. We do not hardcode any values in the code. We retrieve it from this file.

Here is an example of the defining the interested columns for the `cost-and-financing` Excel file -

```yaml
# Dictionary Key to reference our columns of interest
columns_to_keep:
  # Dictionary Key to reference the content category
  cost-and-financing:
    # List defining the columns that we are interested in
    - id
    - Content.Name
    - CostAndFinancing_Title
    - CostAndFinancing_ArticleCatNames
    - CostAndFinancing_CoverImgUrl
    - CostAndFinancing_FullUrl
    - CostAndFinancing_FullUrl2
    - CostAndFinancing_FriendlyUrl
    - CostAndFinancing_CategoryDesc
    - CostAndFinancing_ContentBody
    - CostAndFinancing_ENKeywords
    - CostAndFinancing_FeatureTitle
    - CostAndFinancing_PRName
    - CostAndFinancing_AlternateImageText
    - CostAndFinancing_DateModified
    - CostAndFinancing_NumberofViews
    - CostAndFinancing_LastMonthViewCount
    - CostAndFinancing_LastTwoMonthsView
    - Page Views
    - Engagement Rate
    - Bounce Rate
    - Exit Rate
    - Scroll %
    - "% of Total Views"
    - Cumulative % of Total Views
```

!!! WARNING

    Do not mess the order of the columns in the `parameters_data_processing.yml` file. If you really need to amend it, ensure that the `columns_to_keep` have the same order as `default_columns` (i.e. `columns_to_keep -> default_columns`).
    This is needed because we do not perform any validation in the code to check if the mapping is correctly. This mapping is implicitly defined via this configuration file.

After defining your data variables and the parameters required for your function, we can proceed to the writing our function.

### [`Nodes`](https://github.com/)

Here is where we define our functions to transform our data. A node is merely a step within the Kedro Pipeline that performs a set of transformations. When writing your node functions, you should do the following -

1. Name your node as an `action` (i.e. it should start with a verb).
2. Keep your implementation succinct. If your function requires a multiple functions or has a long implementation, you should consider creating a new Python file and import the main function over to `nodes.py`.
3. Ensure that your input and output variables can be found either in your Data Catalog `catalog.yml` or Parameters `parameters_data_processing.yml`. We prefer to use the same variable names as defined in these configuration files for better clarity.

Once we have created the node(s), we can now integrate them into the Kedro Pipeline.

### [`Pipeline`](https://github.com/)

This is the easiest part of the Kedro pipeline. To integrate the new node, just add a new node function to the pipeline.

!!! WARNING

    The nodes in the Kedro pipeline are ordered. Do not mess the order of these nodes as we are generating the files dynamically from the input files. Each node function has dependencies that are generated by preceding nodes.

Here is an example -

```python
def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=standardize_columns,
                inputs=[
                    "all_contents",
                    "params:columns_to_add",
                    "params:columns_to_keep",
                    "params:default_columns",
                ],
                outputs="all_contents_standardized",
                name="standardize_columns_node",
            ),
            node(
                func=add_data,
                inputs=[
                    "all_contents_standardized",
                    "missing_contents",
                    "params:updated_urls",
                ],
                outputs="all_contents_added",
                name="add_data_node",
            ),
            node(
                func=extract_data,
                inputs=[
                    "all_contents_added",
                    "params:word_count_cutoff",
                    "params:whitelist",
                    "params:blacklist",
                ],
                outputs=["all_contents_extracted", "all_extracted_text"],
                name="extract_data_node",
            ),
            node(
                func=map_data,
                inputs=[
                    "all_contents_extracted",
                    "params:l1_mappings",
                    "params:l2_mappings",
                ],
                outputs="all_contents_mapped",
                name="map_data_node",
            ),
            node(
                func=merge_data,
                inputs="all_contents_mapped",
                outputs="merged_data",
                name="merge_data_node",
            ),
            # Define a node function
            node(
                # The func variable must refer to the node function that you created in nodes.py
                func=new_func_to_add_here,
                # Define your inputs based on what was stated in either catalog.yml or parameters_data_processing.yml. Please note that parameters must have a `params:` prefix defined beforehand
                inputs=[
                    "variable_from_data_catalog_file",
                    "params:variable_from_parameters_config_file"
                ],
                # Define your output(s) based on what was stated in catalog.yml
                outputs=[
                    "variable_from_data_catalog_file"
                ],
                # Name your node function. Please append `node` as a postfix. This name is used for visualising the Kedro pipeline
                name="new_func_node"
            ),
        ]
    )
```
