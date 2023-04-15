from store_documents import StoreDocuments
from search_pipeline import SearchPipeline


def main():
    file_paths = ["funding_opportunities/NOT-AA-20-017.txt",
                  "funding_opportunities/NOT-AA-20-018.txt",
                  "funding_opportunities/NOT-AA-20-019.txt",
                  "funding_opportunities/NOT-AA-20-022.txt",
                  "funding_opportunities/NOT-AA-20-024.txt",
                  "funding_opportunities/NOT-AG-20-041.txt",
                  "funding_opportunities/NOT-AG-21-012.txt",
                  "funding_opportunities/NOT-AG-21-016.txt",
                  "funding_opportunities/NOT-AI-20-044.txt",
                  "funding_opportunities/NOT-AI-21-011.txt",
                  "funding_opportunities/NOT-AI-21-032.txt",
                  "funding_opportunities/NOT-AR-21-006.txt",
                  "funding_opportunities/NOT-AT-20-010.txt",
                  "funding_opportunities/NOT-AT-20-015.txt",
                  "funding_opportunities/NOT-AT-21-001.txt"
                  ]
    doc_store = StoreDocuments("main_faiss")
    # print(doc_store.run(file_paths[0]))
    doc_store.run_batch(file_paths)
    print(len(doc_store.get_all_documents(return_embedding=True)))
    retriever = doc_store.get_retriever()
    search = SearchPipeline(retriever)
    # With reader
    # prediction = search.run(
    #     query="Where is funding for studying alcohol abuse and alcoholism (niaaa)advancing knowledge about the epidemiology of alcohol use",
    #     params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
    # )
    # No reader
    prediction = search.run(
        query="Where is funding for studying alcohol abuse and alcoholism (niaaa)advancing knowledge about the epidemiology of alcohol use",
        params={"Retriever": {"top_k": 10}}
    )
    pred_grant = prediction["documents"][0].meta
    print("------------------------------------")
    print("Try this grant: ", pred_grant["name"])

if __name__ == "__main__":
    main()
