"""Project pipelines."""
from __future__ import annotations
from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
# from orchestration_ml.pipelines.training import pipeline as training_pipeline
# from orchestration_ml.pipelines.processing import pipeline as processing_pipeline
# from orchestration_ml.pipelines.loading import pipeline as loading_pipeline

# %% raw
# def register_pipelines() -> Dict[str, Pipeline]:
#     """Register the project's pipeline.
#
#     Returns:
#         A mapping from a pipeline name to a ``Pipeline`` object.
#
#     """
#     p_processing = processing_pipeline.create_pipeline()
#     p_training = training_pipeline.create_pipeline()
#     p_loading = loading_pipeline.create_pipeline()
#
#     return {
#         "global": Pipeline([p_loading, p_processing, p_training]),
#         "loading": p_loading,
#         "processing": p_processing,
#         "training": p_training
#     }

def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    pipelines["__default__"] = sum(pipelines.values())
    return pipelines