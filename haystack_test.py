from haystack.document_stores.faiss import FAISSDocumentStore

doc_store_name = "test_faiss"
# doc_store = FAISSDocumentStore(sql_url="sqlite:///"+doc_store_name+"_document_store.db")
# doc_store.save(index_path=doc_store_name+"_index.faiss")

doc_store = FAISSDocumentStore(faiss_index_path=doc_store_name+"_index.faiss")

assert doc_store.faiss_index_factory_str == "Flat"
