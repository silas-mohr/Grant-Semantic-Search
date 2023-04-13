from typing import List

from haystack.nodes import PreProcessor, TextConverter
from haystack.document_stores.faiss import FAISSDocumentStore

from file_store_pipeline import FileStorePipeline


class StoreDocuments:
    def __init__(self, doc_store_name: str):
        self.doc_store_name = "database/" + doc_store_name
        self.text_converter = TextConverter()
        self.processor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=True,
            split_by="word",
            split_length=100,
            split_respect_sentence_boundary=False,
            split_overlap=0
        )
        try:
            self.doc_store = FAISSDocumentStore.load(index_path=self.doc_store_name + "_index.faiss",
                                                     config_path=self.doc_store_name + "_config.json")
        except ValueError:
            self.doc_store = FAISSDocumentStore(sql_url="sqlite:///" + self.doc_store_name + "_document_store.db")

        self.p = FileStorePipeline(self.text_converter, self.processor, self.doc_store)

    def run(self, file_path: str):
        return self.p.run(file_path)
        # self.doc_store.save(index_path=self.doc_store_name + "_index.faiss",
        #                     config_path=self.doc_store_name + "_config.json")

    def run_batch(self, file_paths: List[str]):
        self.p.run_batch(file_paths)
        self.doc_store.save(index_path=self.doc_store_name + "_index.faiss",
                            config_path=self.doc_store_name + "_config.json")

    def get_all_documents(self):
        return self.doc_store.get_all_documents()
