---
updated: 4 October 2024
authors:
  - Richmond Sin
---

# @label(func) `standardize_columns`

## Overview

The `standardize_columns` node helps to standardise the columns across multiple Excel files from [`GenAI - Full Content Export.zip`](https://github.com/).

This function takes in a dictionary of dataframes, where each dataframe is associated with a filename. It then standardizes the columns of each dataframe by performing the following steps:

1. Get the content category from the filename.
2. Load the dataframe using the provided partition function.
3. Standardize the column names by selecting and renaming the columns.
4. Mark articles with no content or with dummy content in the `to_remove` column.
5. Add the standardized dataframe to the `all_contents_standardized` dictionary.

The function returns a dictionary mapping content categories to the standardized dataframes.

```python
def standardize_columns(
    all_contents: dict[str, Callable[[], Any]],
    columns_to_add_cfg: dict[str, list[str]],
    columns_to_keep_cfg: dict[str, list[str]],
    default_columns: list[str],
) -> dict[str, pd.DataFrame]:
```

## Parameters

: **`all_contents`** (`dict[str, Callable[[], Any]]`):
A dictionary containing the raw `partitions.PartitionedDataset`where the keys are the filenames and the values loads the raw excel data as `pandas.DataFrame`.
Refer to the [Data Catalog](https://github.com/) for more information.

: **`columns_to_add_cfg`** (`dict[str, list[str]]`):
A dictionary mapping content categories to lists of column names to add. These missing columns are added to facilitate an efficient way of standardising the columns across all dataframes.
This uses the `columns_to_add` parameter from [`parameters_data_processing.yml`](https://github.com/).

: **`columns_to_keep_cfg`** (`dict[str, list[str]]`):
A dictionary mapping content categories to lists of column names to keep. These columns are kept for downstream applications.
This uses the `columns_to_keep` parameter from [`parameters_data_processing.yml`](https://github.com/).

: **`default_columns`** (`list[str]`):
A list of default column names to rename the columns of the dataframes to. These are the column names of the standardized dataframes. All downstream applications will use these columns for further processing.
This uses the `default_columns` parameter from [`parameters_data_processing.yml`](https://github.com/).

## Returns

: **`all_contents_standardized`**:
Returns a set of parquet files corresponding to the content categories. These files are saved at `data/02_intermediate/all_contents_standardized`.
Refer to the `all_contents_standardized` key in the [Data Catalog](https://github.com/).

## Note

: Ensure that the order of the `columns_to_keep` matches the `default_columns` as we do not validate the mappings.
