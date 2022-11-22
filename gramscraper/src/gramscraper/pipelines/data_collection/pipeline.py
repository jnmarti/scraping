"""
This is a boilerplate pipeline 'data_collection'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import crawl_links


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=crawl_links,
            inputs=None,
            outputs="target_links",
            name="link_crawling_node"
        )
    ])
