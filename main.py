import os
import warnings

from grant_search import GrantSearch


def main():
    names = os.listdir(r"funding_opportunities")
    print(len(names))
    warnings.filterwarnings("ignore")

    search = GrantSearch(names[0:50])
    # search.store_documents()
    search.search("Where can I find funding to study the effects of alcohol and alcoholism?")

if __name__ == "__main__":
    main()
