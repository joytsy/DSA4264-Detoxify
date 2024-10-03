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
    # Strip spaces from the texts to remove (but do not modify the 'text' column)
    to_remove_texts = [text.strip() for text in to_remove_texts]

    # Filter out rows where 'text' contains any of the values in to_remove_texts
    removed_deleted_comments_data = data_2020_2021[
        ~data_2020_2021["text"].isin(to_remove_texts)
    ]

    return removed_deleted_comments_data


def remove_nan_values(
    removed_deleted_comments_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Removes rows from the DataFrame that contain NaN values.

    Args:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame with NaN values removed.
    """
    # Remove rows with any NaN values
    removed_nan_comments_data = removed_deleted_comments_data.dropna()

    return removed_nan_comments_data
