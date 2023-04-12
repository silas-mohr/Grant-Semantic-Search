from typing import List

from haystack.pipelines import BaseStandardPipeline
from haystack.document_stores.base import BaseDocumentStore
from haystack.nodes import PreProcessor, TextConverter
from haystack.pipelines.base import Pipeline


class FileStorePipeline(BaseStandardPipeline):
    def __init__(self,
                 document_store: BaseDocumentStore,
                 preprocessor: PreProcessor):
        self.pipeline = Pipeline()
        self.document_store = document_store
        self.preprocessor = preprocessor
        self.pipeline.add_node(component=self.preprocessor, name="PreProcessor", inputs=["Document"])
        # self.pipeline.add_node(component=self.document_store, name="DocumentStore", inputs=["PreProcessor"])

    def run(self, file_path: str):
        return self.pipeline.run(file_paths=[file_path])

    def run_batch(self, file_paths: List[str]):
        return self.pipeline.run_batch(file_paths=file_paths)
