from haystack.nodes import PreProcessor, TextConverter
from haystack.document_stores.faiss import FAISSDocumentStore

from file_store_pipeline import FileStorePipeline

text_converter = TextConverter()
processor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=True,
    split_by="word",
    split_length=100,
    split_respect_sentence_boundary=False,
    split_overlap=0
)

doc_store_name = "test_faiss"
try:
    doc_store = FAISSDocumentStore.load(index_path=doc_store_name+"_index.faiss")
except Exception as ex:
    doc_store = FAISSDocumentStore(sql_url="sqlite:///"+doc_store_name+"_document_store.db")
    print(ex)

assert doc_store.faiss_index_factory_str == "Flat"

p = FileStorePipeline(text_converter, processor, doc_store)

docs = p.run(file_path="test/test_file.txt")
print(docs["documents"][0].meta)

file_paths = ["test/test_file.txt", "test/test_file1.txt"]
docs = p.run_batch(file_paths=file_paths)
print(docs["documents"])

p.draw(path="docstore_pipeline.png")

doc_store.save(index_path=doc_store_name+"_index.faiss")
