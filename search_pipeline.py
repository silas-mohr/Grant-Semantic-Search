from typing import Optional, List
from pathlib import Path

from haystack.pipelines import BaseStandardPipeline
# from haystack.pipelines.base import Pipeline
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline, DocumentSearchPipeline
from haystack.nodes import EmbeddingRetriever


class SearchPipeline(BaseStandardPipeline):
    def __init__(self, retriever: EmbeddingRetriever):
        # self.pipeline = Pipeline()
        self._retriever = retriever

        self._pipe = DocumentSearchPipeline(self._retriever)

    def run(self, query: str, params: Optional[dict] = None, debug: Optional[bool] = None):
        return self._pipe.run(query, params, debug)

    def run_batch(self, queries: List[str], params: Optional[dict] = None, debug: Optional[bool] = None):
        return super().run_batch(queries, params, debug)

    def draw(self, path: Path = Path("pipeline.png")):
        super().draw(path)


# class SearchPipeline(BaseStandardPipeline):
#     def __init__(self, retriever: EmbeddingRetriever):
#         # self.pipeline = Pipeline()
#
#         # Loaded from Hugging Face's model hub (https://huggingface.co/models)
#         self._reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
#         self._retriever = retriever
#
#         self._pipe = ExtractiveQAPipeline(self._reader, self._retriever)
#
#     def run(self, query: str, params: Optional[dict] = None, debug: Optional[bool] = None):
#         return self._pipe.run(query, params, debug)
#
#     def run_batch(self, queries: List[str], params: Optional[dict] = None, debug: Optional[bool] = None):
#         return super().run_batch(queries, params, debug)
#
#     def draw(self, path: Path = Path("pipeline.png")):
#         super().draw(path)