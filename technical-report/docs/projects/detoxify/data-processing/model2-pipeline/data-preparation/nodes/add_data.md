---
updated: 4 October 2024
authors:
  - Richmond Sin
---

# @label(func) `add_data`

## Overview

The `add_data` node helps to add missing HTML text and updated URLs from [`missing_contents.zip`](https://drive.google.com/file/d/1KX7Jsc9LVn6ozsT1P87kTmjVYh4be2j2/view) into the standardised dataframe.

This function takes in a dictionary of dataframes, where each dataframe is associated with a filename. It then adds back the missing and updated data by performing the following steps:

1. Fetches missing content from text files to correct Excel errors.
2. Adds content body to the dataframe for each content category.
3. Updates URLs in the dataframe.
4. Flags articles that should be removed before extraction.

The function returns a dictionary mapping content categories to the updated dataframes.

```python
def add_data(
    all_contents_standardized: dict[str, Callable[[], Any]],
    missing_contents: dict[str, Callable[[], Any]],
    updated_urls: dict[str, dict[int, str]],
) -> dict[str, Callable[[], Any]]:
```

## Parameters

: **`all_contents_standardized`** (`dict[str, Callable[[], Any]]`):
A dictionary where keys are content categories and values are functions that return dataframes of standardized content.
Refer to the [Data Catalog](https://github.com/Synapxe-DNA/healthhub-content-optimization/blob/main/content-optimization/conf/base/catalog.yml) for more information.

: **`missing_contents`** (`dict[str, Callable[[], Any]]`):
A dictionary where keys are file paths and values are functions that load the content of text files.
Refer to the [Data Catalog](https://github.com/Synapxe-DNA/healthhub-content-optimization/blob/main/content-optimization/conf/base/catalog.yml) for more information.

: **`updated_urls`** (`dict[str, dict[int, str]]`):
A dictionary where keys are content categories and values are dictionaries mapping the article IDs to updated URLs.
This uses the `columns_to_keep` parameter from [`parameters_data_processing.yml`](https://github.com/Synapxe-DNA/healthhub-content-optimization/blob/main/content-optimization/conf/base/parameters_data_processing.yml).

## Returns

: **`all_contents_added`**:
Returns a set of parquet files corresponding to the content categories. These files are saved at `data/02_intermediate/all_contents_added`. Refer to the `all_contents_added` key in the [Data Catalog](https://github.com/Synapxe-DNA/healthhub-content-optimization/blob/main/content-optimization/conf/base/catalog.yml)

## Note

: Some articles will be flagged for removal before extraction. Refer to the `flag_articles_to_remove_before_extraction` function in [`utils.py`](https://github.com/Synapxe-DNA/healthhub-content-optimization/blob/main/content-optimization/src/content_optimization/pipelines/data_processing/utils.py) for more information.
