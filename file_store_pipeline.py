from typing import List

from haystack.pipelines import BaseStandardPipeline
from haystack.document_stores.base import BaseDocumentStore
from haystack.nodes import PreProcessor, TextConverter
from haystack.pipelines.base import Pipeline


class FileStorePipeline(BaseStandardPipeline):
    def __init__(self,
                 document_store: BaseDocumentStore,
                 preprocessor: PreProcessor,
                 text_converter: TextConverter):
        self.pipeline = Pipeline() # Underlying Pipeline
        self.document_store = document_store # Document store to hold all process Documents
        self.preprocessor = preprocessor # Preprocessor to clean the Documents
        self.text_converter = text_converter # Converts from txt file to Haystack Document
        self.pipeline.add_node(component=self.text_converter, name="TextConverter", inputs=["File"])
        self.pipeline.add_node(component=self.preprocessor, name="PreProcessor", inputs=["TextConverter"])
        self.pipeline.add_node(component=self.document_store, name="DocumentStore", inputs=["PreProcessor"])

    def run(self, file_path: str):
        # Add name metadata to file from first line in file
        with open(file_path) as f:
            meta = {"name": f.readline().strip()}

        # Run pipeline
        return self.pipeline.run(file_paths=[file_path], meta=meta)

    def run_batch(self, file_paths: List[str]):
        # Add name metadata to each file in file_paths from first line in each file
        meta = []
        for file_path in file_paths:
            with open(file_path) as f:
                meta.append({"name": f.readline().strip()})

        # Run pipeline
        return self.pipeline.run_batch(file_paths=file_paths, meta=meta)
