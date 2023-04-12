from haystack.nodes import PreProcessor
from haystack.schema import Document
from haystack.document_stores.faiss import FAISSDocumentStore

from file_store_pipeline import FileStorePipeline

processor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=True,
    split_by="word",
    split_length=100,
    split_respect_sentence_boundary=False,
    split_overlap=0
)

docs = []
with open("funding_opportunities/NOT-AA-20-017.txt") as f:
    name = f.readline().strip()
    content = f.readline()
    docs.append(Document(content=content, meta={"name": name}))

docs = processor.process(docs)
for i in docs:
    print(i.meta)

doc_store = FAISSDocumentStore()

p = FileStorePipeline(doc_store, processor)

p.run()
