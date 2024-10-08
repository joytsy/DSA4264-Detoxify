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
        # Remove all characters except alphabets, digits, whitespace, quotes (single and double), exclamation marks, full stops, commas, and colons
        cleaned_text = re.sub(
            r"[^\w\s\"'\.,!:]", "", text
        )  # Add ':' to the allowed characters

        # Remove multiple spaces
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)

        # Manually remove leading spaces
        cleaned_text = re.sub(r"^\s+", "", cleaned_text)

        # Manually remove trailing spaces
        cleaned_text = re.sub(r"\s+$", "", cleaned_text)

        return cleaned_text

    clean_text_column_data = removed_nan_text_data.copy()

    # Apply the cleaning function to the 'text' column without progress tracking
    clean_text_column_data["text"] = clean_text_column_data["text"].apply(clean_text)

    return clean_text_column_data


def second_removal_nan_values(
    clean_text_column_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Removes rows from the DataFrame that contain NaN values.

    Args:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame with NaN values removed.
    """
    # Remove rows with any NaN values
    second_removal_nan_text_data = clean_text_column_data.dropna()

    return second_removal_nan_text_data


def process_timestamp_to_year(
    second_removal_nan_text_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Converts the 'timestamp' column in the DataFrame to datetime,
    extracts the year, and handles NaN values.

    Parameters:
    data (pd.DataFrame): Input DataFrame containing the 'timestamp' column.

    Returns:
    pd.DataFrame: Updated DataFrame with the extracted 'year' column.
    """
    process_timestamp_to_year_data = second_removal_nan_text_data
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
    processed_ids = set()  # Track processed IDs to avoid duplicating threads
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
        group = group.reset_index(drop=True)  # reset index to clean up indexing

        for idx, current_comment in group.iterrows():
            # Skip comments that have already been processed in a thread
            if current_comment["id"] in processed_ids:
                continue

            # Start tracking the top-level comment details
            top_comment_timestamp = current_comment["timestamp"]
            top_comment_username = current_comment["username"]
            top_comment_link = current_comment["link"]
            top_comment_parent_id = current_comment["parent_id"]
            top_comment_id = current_comment["id"]
            top_comment_subreddit_id = current_comment["subreddit_id"]
            top_comment_moderation = current_comment["moderation"]
            top_comment_year = current_comment["year"]

            # Initialize the thread text and add the first comment
            thread_text = (
                f"id of {current_comment['id']} said this: {current_comment['text']}.\n"
            )
            processed_ids.add(current_comment["id"])
            concatenated_count = 1  # Start count for the thread

            # Track if this is a complete thread
            complete_thread = current_comment["parent_id"] == current_comment["link_id"]

            # Use a while loop to concatenate replies, ensuring comments are processed only once
            while True:
                # Use the reply dictionary to find replies efficiently
                next_comments = reply_dict.get(f"t1_{current_comment['id']}", [])
                if next_comments:
                    current_comment = next_comments[0]  # Get the next reply
                    # Only process this comment if it's not processed already
                    if current_comment["id"] not in processed_ids:
                        # Append the next comment using varied bridging words
                        thread_text += f"id of {current_comment['id']} replied to id of {current_comment['parent_id'][3:]}: {current_comment['text']}\n"
                        processed_ids.add(current_comment["id"])
                        concatenated_count += 1
                    else:
                        break  # If comment has already been processed, break to avoid duplication
                else:
                    break  # Stop once no further replies are found

            # Append the result with the concatenated thread
            result.append(
                {
                    "text": thread_text.strip(),
                    "timestamp": top_comment_timestamp,
                    "username": top_comment_username,
                    "link": top_comment_link,
                    "link_id": link_id,
                    "parent_id": top_comment_parent_id,
                    "id": top_comment_id,
                    "subreddit_id": top_comment_subreddit_id,
                    "moderation": top_comment_moderation,
                    "year": top_comment_year,
                    "concatenated_count": concatenated_count,
                    "complete_thread": complete_thread,
                }
            )

    # Create a DataFrame for the concatenated threads
    concatenated_texts_data = pd.DataFrame(result)

    # Return the processed data
    return concatenated_texts_data


def clean_concatenated_texts(concatenated_texts_data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the concatenated_texts_data by removing all occurrences of 'gt ' from the 'text' column.

    Args:
        concatenated_texts_data (pd.DataFrame): DataFrame containing concatenated comment threads.

    Returns:
        pd.DataFrame: Cleaned DataFrame with 'gt ' removed from the 'text' column.
    """
    clean_concatenated_texts_data = concatenated_texts_data

    # Remove all occurrences of 'gt ' from the 'text' column
    clean_concatenated_texts_data["text"] = clean_concatenated_texts_data[
        "text"
    ].str.replace("gt ", "", regex=False)

    return clean_concatenated_texts_data
