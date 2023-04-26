from typing import Optional, List

from store_documents import StoreDocuments
from search_pipeline import  SearchPipeline

class GrantSearch:
    def __init__(self, file_paths: List[str], doc_store_name: Optional[str] = "main_faiss"):
        self._file_paths = file_paths
        self._doc_store = StoreDocuments(doc_store_name)
        self._retriever = self._doc_store.get_retriever()
        self._faiss = self._doc_store.get_doc_store()
        self._search = SearchPipeline(self._retriever, self._faiss)

    def store_documents(self):
        self._doc_store.run_batch(self._file_paths)

    def search(self, query: str):
        prediction = self._search.run(
            query=query,
            params={"EmbeddingRetriever": {"top_k":10}, "DensePassageRetriever": {"top_k": 10}, "Ranker": {"top_k": 5}}
        )
        print("Your query:", query)
        for i, grant in enumerate(prediction["documents"]):
            grant_meta = grant.meta
            print("-" * 36)
            print("Result #", i+1, sep="")
            print("Try this grant:", grant_meta["name"])
            print("Grant number:  ", grant_meta["grant_num"])
            print("Link:", grant_meta["url"])
            print("-" * 36)
