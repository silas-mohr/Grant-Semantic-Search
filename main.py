from store_documents import StoreDocuments


def main():
    file_paths = ["test/test_file.txt", "test/test_file1.txt"]
    doc_store = StoreDocuments("main_faiss")
    print(doc_store.run(file_paths[0]))
    # print(doc_store.get_all_documents()[0])


if __name__ == "__main__":
    main()
