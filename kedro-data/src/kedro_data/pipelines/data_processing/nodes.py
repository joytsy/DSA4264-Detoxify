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
        merged_raw_data (pd.DataFrame): Merged DataFrame containing social media text data from 2020-2023.
        to_remove_texts (List[str]): List of text entries (e.g., '[deleted]', '[removed]') to filter out.

    Returns:
        pd.DataFrame: Filtered DataFrame after removing the specified text values.
    """
    to_remove_texts = [text.strip() for text in to_remove_texts]

    # Apply filtering without progress tracking, since it's unnecessary for `isin`
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
    Cleans the 'text' column of a DataFrame by removing unwanted characters,
    replacing specific patterns, and removing excess spaces.

    Args:
        removed_nan_text_data (pd.DataFrame): Input DataFrame with the 'text' column to be cleaned.

    Returns:
        pd.DataFrame: DataFrame with the cleaned 'text' column.
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

    clean_text_column_data = removed_nan_text_data.copy()

    # Apply the cleaning function to the 'text' column without progress tracking
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
    Filters the input DataFrame by removing rows where the 'username' column contains specific values like '[deleted]' or '[removed]'.

    Args:
        process_timestamp_to_year_data (pd.DataFrame): DataFrame with the extracted year column.
        to_remove_texts (List[str]): List of username entries (e.g., '[deleted]', '[removed]') to filter out.

    Returns:
        pd.DataFrame: Filtered DataFrame after removing the specified username values.
    """
    to_remove_texts = [text.strip() for text in to_remove_texts]

    # Filter out rows without progress tracking
    removed_deleted_username_data = process_timestamp_to_year_data[
        ~process_timestamp_to_year_data["username"].isin(to_remove_texts)
    ]

    return removed_deleted_username_data


def concatenate_texts(removed_deleted_username_data: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the input DataFrame by concatenating comment threads and creating
    a complete or incomplete thread summary using a dictionary lookup.

    Args:
        removed_deleted_username_data (pd.DataFrame): DataFrame with comments after filtering out removed/deleted users.

    Returns:
        pd.DataFrame: DataFrame with concatenated comment threads.
    """
    result = []
    processed_ids = set()  # Track processed IDs instead of removing rows immediately
    reply_dict = {}  # Dictionary to store replies based on parent_id

    # Build the reply dictionary for fast lookup
    for idx, row in removed_deleted_username_data.iterrows():
        parent_id = row["parent_id"]
        if parent_id not in reply_dict:
            reply_dict[parent_id] = []
        reply_dict[parent_id].append(row)

    # Group rows by link_id to find Reddit posts (threads can be within these)
    grouped = removed_deleted_username_data.groupby("link_id")

    # Process each group (link_id) of posts
    for link_id, group in grouped:
        group = group.reset_index()  # reset index here to get clean integer indexing

        for idx, current_comment in group.iterrows():
            # Skip comments that have already been processed in a thread
            if current_comment["id"] in processed_ids:
                continue

            thread_text = (
                f"id of {current_comment['id']} said this: {current_comment['text']}.\n"
            )
            processed_ids.add(current_comment["id"])
            concatenated_count = 1  # Start count for the thread

            # Track if this is a complete thread
            complete_thread = current_comment["parent_id"] == current_comment["link_id"]

            # Try to find and concatenate linked replies using the reply dictionary
            while True:
                # Use the reply dictionary to find replies efficiently
                next_comments = reply_dict.get(f"t1_{current_comment['id']}", [])
                if next_comments:
                    current_comment = next_comments[0]  # Get the next reply
                    thread_text += f"id of {current_comment['id']} replied to id of {current_comment['parent_id'][3:]}: {current_comment['text']}\n"
                    processed_ids.add(current_comment["id"])
                    concatenated_count += 1
                else:
                    break  # Stop once no further replies are found

            # Append the result
            result.append(
                {
                    "text": thread_text.strip(),  # Remove trailing newlines
                    "timestamp": current_comment[
                        "timestamp"
                    ],  # Use the timestamp of the first comment
                    "username": current_comment["username"],
                    "link": current_comment["link"],
                    "link_id": link_id,
                    "parent_id": current_comment[
                        "parent_id"
                    ],  # Keep parent_id of top comment
                    "id": current_comment["id"],  # Keep id of the top comment
                    "subreddit_id": current_comment["subreddit_id"],
                    "moderation": current_comment["moderation"],
                    "year": current_comment["year"],
                    "concatenated_count": concatenated_count,  # Number of comments in the thread
                    "complete_thread": complete_thread,  # Mark whether the thread is complete
                }
            )

    # Create a DataFrame for the concatenated threads
    concatenated_texts_data = pd.DataFrame(result)

    # Return the processed data
    return concatenated_texts_data
