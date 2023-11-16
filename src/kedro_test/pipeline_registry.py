"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    default_pipeline = sum(pipelines.values())
    assert isinstance(default_pipeline, Pipeline)  # for typechecking
    pipelines["__default__"] = default_pipeline
    return pipelines
