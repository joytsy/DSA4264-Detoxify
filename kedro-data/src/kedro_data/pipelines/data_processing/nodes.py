"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.8
"""

from typing import List
import re
import pandas as pd


def merged_raw(
    data_2020_2021: pd.DataFrame,
    data_2022_2023: pd.DataFrame,
) -> pd.DataFrame:
    merged_raw_data = pd.concat([data_2020_2021, data_2022_2023], ignore_index=True)

    return merged_raw_data


def remove_deleted_text(
    merged_raw_data: pd.DataFrame,
    to_remove_texts: List[str],
) -> pd.DataFrame:
    """
    Filters the input DataFrame by removing rows where the 'text' column contains specific values like '[deleted]' or '[removed]'.

    Args:
        data_2020_2021 (pd.DataFrame): DataFrame containing social media text from 2020-2021.
        to_remove_texts (List[str]): List of text entries (e.g., '[deleted]', '[removed]') to filter out.

    Returns:
        pd.DataFrame: Filtered DataFrame after removing the specified text values.
    """
    # Strip spaces from the texts to remove (but do not modify the 'text' column)
    to_remove_texts = [text.strip() for text in to_remove_texts]

    # Filter out rows where 'text' contains any of the values in to_remove_texts
    removed_deleted_text_data = merged_raw_data[
        ~merged_raw_data["text"].isin(to_remove_texts)
    ]

    return removed_deleted_text_data


def remove_nan_values(
    removed_deleted_text_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Removes rows from the DataFrame that contain NaN values.

    Args:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame with NaN values removed.
    """
    # Remove rows with any NaN values
    removed_nan_text_data = removed_deleted_text_data.dropna()

    return removed_nan_text_data


def clean_text_column(removed_nan_text_data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the 'text' column of a dataframe by removing unwanted characters,
    replacing specific patterns, and removing excess spaces.

    Args:
        data: The input dataframe containing a 'text' column to be cleaned.

    Returns:
        A dataframe with the cleaned 'text' column.
    """

    def clean_text(text):
        # Replace '>' at the start of the line with 'Quoting'
        cleaned_text = re.sub(r"^>\s*", "Quoting: ", text, flags=re.MULTILINE)

        # Remove \> (backslash followed by greater-than sign)
        cleaned_text = cleaned_text.replace(r"\>", "")

        # Remove all weird Unicode characters, keeping only alphabets, digits, and whitespace
        cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", "", cleaned_text)

        # Remove multiple spaces
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)

        # Remove leading spaces
        cleaned_text = re.sub(r"^\s+", "", cleaned_text)

        # Remove trailing spaces
        cleaned_text = re.sub(r"\s+$", "", cleaned_text)

        return cleaned_text

    clean_text_column_data = removed_nan_text_data

    # Apply the cleaning function to the 'text' column
    clean_text_column_data["text"] = clean_text_column_data["text"].apply(clean_text)

    return clean_text_column_data


def process_timestamp_to_year(clean_text_column_data: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the 'timestamp' column in the DataFrame to datetime,
    extracts the year, and handles NaN values.

    Parameters:
    data (pd.DataFrame): Input DataFrame containing the 'timestamp' column.

    Returns:
    pd.DataFrame: Updated DataFrame with the extracted 'year' column.
    """
    process_timestamp_to_year_data = clean_text_column_data
    # Convert 'timestamp' to datetime
    process_timestamp_to_year_data["timestamp"] = pd.to_datetime(
        process_timestamp_to_year_data["timestamp"], errors="coerce"
    )

    # Extract the year from the timestamp
    process_timestamp_to_year_data["year"] = process_timestamp_to_year_data[
        "timestamp"
    ].dt.year

    # Convert year to nullable integer (Int64) and handle NaN values
    process_timestamp_to_year_data["year"] = pd.to_numeric(
        process_timestamp_to_year_data["year"], errors="coerce"
    ).astype("Int64")

    return process_timestamp_to_year_data


def remove_deleted_username(
    process_timestamp_to_year_data: pd.DataFrame,
    to_remove_texts: List[str],
) -> pd.DataFrame:
    """
    Filters the input DataFrame by removing rows where the 'text' column contains specific values like '[deleted]' or '[removed]'.

    Args:
        merged_raw_data (pd.DataFrame): DataFrame from 2020 to 2023.
        to_remove_texts (List[str]): List of text entries (e.g., '[deleted]', '[removed]') to filter out.

    Returns:
        pd.DataFrame: Filtered DataFrame after removing the specified text values.
    """
    # Strip spaces from the texts to remove (but do not modify the 'text' column)
    to_remove_texts = [text.strip() for text in to_remove_texts]

    # Filter out rows where 'text' contains any of the values in to_remove_texts
    removed_deleted_username_data = process_timestamp_to_year_data[
        ~process_timestamp_to_year_data["username"].isin(to_remove_texts)
    ]

    return removed_deleted_username_data
