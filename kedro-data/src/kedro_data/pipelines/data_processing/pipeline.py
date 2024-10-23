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
    clean_gt_texts,
    # remove_stopwords_and_lowercase,
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
                ],
                name="removed_deleted_username_node",
            ),
            node(
                func=clean_gt_texts,
                inputs=[
                    "removed_deleted_username_data",
                ],
                outputs="clean_gt_texts_data",
                name="clean_gt_texts_node",
            ),
            # node(
            #     func=remove_stopwords_and_lowercase,
            #     inputs=[
            #         "clean_gt_texts_data",
            #     ],
            #     outputs="remove_stopwords_and_lowercase_data",
            #     name="remove_stopwords_and_lowercase_node",
            # ),
        ]
    )
