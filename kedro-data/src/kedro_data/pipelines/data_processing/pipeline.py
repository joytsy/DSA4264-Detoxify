"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.8
"""

from kedro.pipeline import Pipeline, node, pipeline

from kedro_data.pipelines.data_processing.nodes import (
    merged_raw,
    remove_deleted_text,
    remove_nan_values,
    clean_text_column,
    process_timestamp_to_year,
    remove_deleted_username,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=merged_raw,
                inputs=[
                    "data_2020_2021",
                    "data_2022_2023",  # The dataset name as per the catalog.yml
                ],
                outputs="merged_raw_data",  # Output dataset name
                name="merged_raw_node",
            ),
            node(
                func=remove_deleted_text,
                inputs=[
                    "merged_raw_data",  # The dataset name as per the catalog.yml
                    "params:to_remove_texts",  # Parameters defined in parameters.yml
                ],
                outputs="removed_deleted_text_data",  # Output dataset name
                name="remove_deleted_text_node",
            ),
            node(
                func=remove_nan_values,
                inputs=[
                    "removed_deleted_text_data",
                ],
                outputs="removed_nan_text_data",
                name="remove_nan_text_node",
            ),
            node(
                func=clean_text_column,
                inputs=[
                    "removed_nan_text_data",
                ],
                outputs="clean_text_column_data",
                name="clean_text_column_node",
            ),
            node(
                func=process_timestamp_to_year,
                inputs=[
                    "clean_text_column_data",
                ],
                outputs="process_timestamp_to_year_data",
                name="process_timestamp_to_year_node",
            ),
            node(
                func=remove_deleted_username,
                inputs=[
                    "process_timestamp_to_year_data",
                    "params:to_remove_texts",
                ],
                outputs="removed_deleted_username_data",
                name="removed_deleted_username_node",
            ),
        ]
    )
