"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.8
"""

from kedro.pipeline import Pipeline, node, pipeline

from kedro_data.pipelines.data_processing.nodes import remove_deleted_comments


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=remove_deleted_comments,
                inputs=[
                    "data_2020_2021",  # The dataset name as per the catalog.yml
                    "params:to_remove_texts",  # Parameters defined in parameters.yml
                ],
                outputs="removed_deleted_comments_data",  # Output dataset name
                name="remove_deleted_comments_node",
            ),
        ]
    )
