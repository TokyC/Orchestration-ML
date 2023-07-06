from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    clean_dataset,
    create_features,
    create_dataset,
    encode_features,
    split_dataset,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=clean_dataset,
                inputs="primary",
                outputs=dict(dataset="dataset_cleaned"),
                name="clean_dataset_node",
            ),
            node(
                func=create_features,
                inputs=["dataset_cleaned"],
                outputs=dict(dataset="dataset_features"),
                name="create_features_node",
            ),
            node(
                func=create_dataset,
                inputs=["dataset_features", "dataset_cleaned"],
                outputs=dict(dataset="dataset_final"),
                name="create_dataset_node",
            ),
            node(
                func=encode_features,
                inputs="dataset_final",
                outputs=dict(dataset="dataset_encoded"),
                name="encode_features_node",
            ),
            node(
                func=split_dataset,
                inputs=["dataset_encoded", "params:test_ratio"],
                outputs=dict(
                    X_train="X_train",
                    y_train="y_train",
                    X_test="X_test",
                    y_test="y_test",
                ),
                name="split_dataset_node",
            ),
        ],
        tags="processing",
    )
