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
    second_removal_nan_values,
    process_timestamp_to_year,
    remove_deleted_username,
    concatenate_texts,
    clean_concatenated_texts,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=merged_raw,
                inputs=[
                    "data_2020_2021",
                    "data_2022_2023",
                ],
                outputs="merged_raw_data",
                name="merged_raw_node",
            ),
            node(
                func=remove_deleted_text,
                inputs=[
                    "merged_raw_data",
                    "params:to_remove_texts",
                ],
                outputs="removed_deleted_text_data",
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
                func=second_removal_nan_values,
                inputs=[
                    "clean_text_column_data",
                ],
                outputs="second_removal_nan_text_data",
                name="second_removal_nan_text_node",
            ),
            node(
                func=process_timestamp_to_year,
                inputs=[
                    "second_removal_nan_text_data",
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
                outputs=[
                    "removed_deleted_username_data",
                    "single_comment_data",
                ],  # Two outputs
                name="removed_deleted_username_node",
            ),
            node(
                func=concatenate_texts,
                inputs=[
                    "removed_deleted_username_data",
                ],
                outputs=["concatenated_texts_data"],
                name="concatenate_texts_node",
            ),
            node(
                func=clean_concatenated_texts,
                inputs=[
                    "concatenated_texts_data",
                ],
                outputs="clean_concatenated_texts_data",
                name="clean_concatenate_texts_node",
            ),
        ]
    )
