from store_documents import StoreDocuments
from search_pipeline import  SearchPipeline

class GrantSearch:
    def __init__(self, file_paths):
        self._file_paths = file_paths


import os

names = os.listdir(r"funding_opportunities")
print(len(names))
