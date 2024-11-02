---
updated: 4 October 2024
authors:
  - Richmond Sin
---

# Overview

The Data Processing Pipeline consists of 5 nodes:

1. @label(func) `standardize_columns`: Standardise the column names of multiple dataframes loaded from the Excel Files
2. @label(func) `add_data`: Add back the missing contents and updated URLs to the standardised dataframes
3. @label(func) `extract_data`: Extract tables, links, headers and content from the Raw HTML text
4. @label(func) `map_data`: Map the articles to its new L1 and L2 IA mappings based on its `content_category` and `article_category_names`
5. @label(func) `merge_data`: Merge all the partitioned dataframes (across all content categories) in to a single parquet file `merged_data.parquet`.
