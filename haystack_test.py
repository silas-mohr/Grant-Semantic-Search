import os

import pandas as pd
import numpy as np

from haystack.document_stores.faiss import FAISSDocumentStore
from haystack.pipelines import Pipeline
from haystack.nodes import PreProcessor, TextConverter, EmbeddingRetriever

# df = pd.read_csv("datasets/arxiv_short.csv")
# print(df.head())
# print(df.isnull().sum())

text_converter = TextConverter()
preprocessor = PreProcessor()
document_store = FAISSDocumentStore()

p = Pipeline()
p.add_node(component=text_converter, name="TextConverter", inputs=["File"])
p.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])

result = p.run(file_paths=["funding_opportunities/NOT-AA-20-017.txt"])
