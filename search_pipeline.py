from haystack.pipelines import BaseStandardPipeline
from haystack.pipelines.base import Pipeline


class SearchPipeline(BaseStandardPipeline):
    def __init__(self):
        self.pipeline = Pipeline()