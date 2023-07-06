"""
This is a boilerplate pipeline 'training'
generated using Kedro 0.18.11
"""

from kedro.pipeline import Pipeline, node
from .nodes import auto_ml, run_mlflow


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                auto_ml,
                ["X_train", "y_train", "X_test", "y_test", "params:automl_max_evals"],
                dict(model="model"),
            ),
            node(
                func=run_mlflow,
                inputs="model",
                outputs="status",
                name="run_mlflow_node"
            )
        ]
    )
