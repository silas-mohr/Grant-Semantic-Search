from typing import Optional, List
from pathlib import Path

from haystack.document_stores import BaseDocumentStore
from haystack.pipelines import BaseStandardPipeline
from haystack.pipelines.base import Pipeline
from haystack.nodes import SentenceTransformersRanker, JoinDocuments, TransformersQueryClassifier, EmbeddingRetriever, DensePassageRetriever


class SearchPipeline(BaseStandardPipeline):
    def __init__(self, emb_retriever: EmbeddingRetriever, doc_store: BaseDocumentStore):
        self._doc_store = doc_store
        self._pipe = Pipeline()
        self._query_classifier = TransformersQueryClassifier(model_name_or_path="shahrukhx01/bert-mini-finetune-question-detection")
        self._emb_retriever = emb_retriever
        self._dp_retriever = DensePassageRetriever(document_store=self._doc_store,
                                                   query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
                                                   passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base"
                                                   )
        self._joiner = JoinDocuments(join_mode="concatenate")
        self._ranker = SentenceTransformersRanker(model_name_or_path="cross-encoder/ms-marco-MiniLM-L-12-v2")

        self._pipe.add_node(component=self._query_classifier, name="QueryClassifier", inputs=["Query"])
        self._pipe.add_node(component=self._emb_retriever, name="EmbeddingRetriever", inputs=["QueryClassifier.output_1"])
        self._pipe.add_node(component=self._dp_retriever, name="DensePassageRetriever", inputs=["QueryClassifier.output_2"])
        self._pipe.add_node(component=self._joiner, name="Joiner", inputs=["EmbeddingRetriever", "DensePassageRetriever"])
        self._pipe.add_node(component=self._ranker, name="Ranker", inputs=["Joiner"])

    def run(self, query: str, params: Optional[dict] = None, debug: Optional[bool] = None):
        return self._pipe.run(query, params, debug)

    def run_batch(self, queries: List[str], params: Optional[dict] = None, debug: Optional[bool] = None):
        return super().run_batch(queries, params, debug)

    def draw(self, path: Path = Path("pipeline.png")):
        self._pipe.draw(path)
