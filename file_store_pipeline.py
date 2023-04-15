from typing import List

from haystack.document_stores.faiss import FAISSDocumentStore
from haystack.nodes import PreProcessor, TextConverter
from haystack.schema import Document
from haystack.nodes import EmbeddingRetriever


class FileStorePipeline:
    def __init__(self,
                 text_converter: TextConverter,
                 preprocessor: PreProcessor,
                 document_store: FAISSDocumentStore,
                 doc_store_name: str):
        self.document_store = document_store  # Document store to hold all process Documents
        self.preprocessor = preprocessor  # Preprocessor to clean the Documents
        self.text_converter = text_converter  # Converts from txt file to Haystack Document
        self.doc_store_name = doc_store_name

    def run(self, file_path: str, embedding_retriever: EmbeddingRetriever) -> Document:
        return self.run_batch([file_path], embedding_retriever)[0]

    def run_batch(self, file_paths: List[str], embedding_retriever: EmbeddingRetriever) -> List[Document]:
        # Add name metadata to each file in file_paths from first line in each file
        documents = []
        for file_path in file_paths:
            with open(file_path) as f:
                meta = {"name": f.readline().strip()}
                content = f.readline()
                documents.append(Document(content=content, meta=meta))
        documents = self.preprocessor.process(documents)
        self.document_store.write_documents(documents)
        self.document_store.update_embeddings(embedding_retriever)
        self.document_store.save(index_path=self.doc_store_name + "_index.faiss",
                                 config_path=self.doc_store_name + "_config.json")
        return documents
