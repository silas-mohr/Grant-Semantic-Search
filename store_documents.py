from typing import List, Dict, Optional

from haystack.document_stores import BaseDocumentStore
from haystack.nodes import PreProcessor, TextConverter
from haystack.document_stores.faiss import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.schema import Document, FilterType

from file_store_pipeline import FileStorePipeline


class StoreDocuments:
    def __init__(self, doc_store_name: str):
        self._doc_store_name = "database/" + doc_store_name
        self._text_converter = TextConverter()
        self._processor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=True,
            split_by="word", split_length=100,
            split_respect_sentence_boundary=False,
            split_overlap=0
        )
        try:
            self._doc_store = FAISSDocumentStore.load(index_path=self._doc_store_name + "_index.faiss",
                                                      config_path=self._doc_store_name + "_config.json")
        except ValueError:
            self._doc_store = FAISSDocumentStore(sql_url="sqlite:///" + self._doc_store_name + "_document_store.db",
                                                 similarity="dot_product")

        self._p = FileStorePipeline(self._text_converter, self._processor, self._doc_store, self._doc_store_name)
        self._emb_retriever = EmbeddingRetriever(document_store=self._doc_store,
                                                 embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1"
                                                 )

    def run(self, file_path: str) -> Document:
        return self._p.run(file_path, self._emb_retriever)

    def run_batch(self, file_paths: List[str]) -> List[Document]:
        return self._p.run_batch(file_paths, self._emb_retriever)

    def get_all_documents(self,
                          index: Optional[str] = None,
                          filters: Optional[FilterType] = None,
                          return_embedding: Optional[bool] = None,
                          batch_size: int = 10_000,
                          headers: Optional[Dict[str, str]] = None
                          ) -> List[Document]:
        return self._doc_store.get_all_documents(index, filters, return_embedding, batch_size, headers)

    def get_retriever(self) -> EmbeddingRetriever:
        return self._emb_retriever

    def get_doc_store(self) -> BaseDocumentStore:
        return self._doc_store
