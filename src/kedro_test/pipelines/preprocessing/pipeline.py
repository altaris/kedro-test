"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    create_model_input_table,
    preprocess_companies,
    preprocess_shuttles,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_companies,
                inputs="companies_raw",
                outputs="companies_ds",
                name="preprocess_companies_node",
            ),
            node(
                func=preprocess_shuttles,
                inputs="shuttles_raw",
                outputs="shuttles_ds",
                name="preprocess_shuttles_node",
            ),
            node(
                func=create_model_input_table,
                inputs=[
                    "shuttles_ds",
                    "companies_ds",
                    "reviews_raw",
                ],
                outputs="model_input_ds",
                name="create_model_input_ds_node",
            ),
        ]
    )
