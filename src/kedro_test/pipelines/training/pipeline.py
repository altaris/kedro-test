"""
This is a boilerplate pipeline 'training'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import create_datamodule, create_model, train_model, evaluate_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_datamodule,
                inputs=["model_input_ds", "params:datamodule"],
                outputs="model_input_dm",
                name="create_datamodule_node",
            ),
            node(
                func=create_model,
                inputs=["params:model"],
                outputs="model_new",
                name="create_model_node",
            ),
            node(
                func=train_model,
                inputs=["model_new", "model_input_dm", "params:training"],
                outputs="model",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["model", "model_input_dm"],
                outputs="metrics",
                name="evaluate_model_node",
            ),
        ]
    )
