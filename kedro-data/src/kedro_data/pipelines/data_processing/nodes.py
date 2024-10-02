"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.8
"""

from typing import List

import pandas as pd


def remove_deleted_comments(
    data_2020_2021: pd.DataFrame,
    to_remove_texts: List[str],
) -> pd.DataFrame:
    """
    Filters the input DataFrame by removing rows where the 'text' column contains specific values like '[deleted]' or '[removed]'.

    Args:
        data_2020_2021 (pd.DataFrame): DataFrame containing social media comments from 2020-2021.
        to_remove_texts (List[str]): List of text entries (e.g., '[deleted]', '[removed]') to filter out.

    Returns:
        pd.DataFrame: Filtered DataFrame after removing the specified text values.
    """
    # Filter out rows where 'text' contains '[deleted]' or '[removed]'
    removed_deleted_comments_data = data_2020_2021[
        ~data_2020_2021["text"].isin(to_remove_texts)
    ]

    return removed_deleted_comments_data
