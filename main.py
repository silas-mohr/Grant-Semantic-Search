from pathlib import Path

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
    doc_store.run_batch(file_paths)
    # print(len(doc_store.get_all_documents(return_embedding=True)))
    retriever = doc_store.get_retriever()
    doc_store = doc_store.get_doc_store()
    search = SearchPipeline(retriever, doc_store)
    query = "Where is funding for studying alcohol abuse and alcoholism?"
    # With reader
    # prediction = search.run(
    #     query=query,
    #     params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
    # )
    # No reader
    prediction = search.run(
        query=query,
        params={"EmbeddingRetriever": {"top_k": 5}, "DPRRetriever": {"top_k": 5}}
    )
    print("Your query:", query)
    for i, grant in enumerate(prediction["documents"]):
        pred_grant = grant.meta
        print("------------------------------------")
        print("Result #", i, sep="")
        print("Try this grant:", pred_grant["name"])
        print("Grant number:  ", pred_grant["grant_num"])
        print("------------------------------------")

    # search.draw(Path("pipeline_visualizations/search_pipeline.png"))

if __name__ == "__main__":
    main()
