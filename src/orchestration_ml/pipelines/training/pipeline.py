"""
This is a boilerplate pipeline 'training'
generated using Kedro 0.18.11
"""

from kedro.pipeline import Pipeline, node
from .nodes import auto_ml


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                auto_ml,
                ["X_train", "y_train", "X_test", "y_test", "params:automl_max_evals"],
                dict(model="model"),
            )
        ]
    )
