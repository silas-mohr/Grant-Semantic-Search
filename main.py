import os
import warnings
import argparse as ap

from grant_search import GrantSearch


def parsing():
    try:
        parser = ap.ArgumentParser(description='Semantic Search for Government Grants Within Healthcare', allow_abbrev=False)
        parser.add_argument('update', help='should the document store be updated?', type=int)
        parser.add_argument('-q', '--query', help='the query to search', type=str)
        parser.add_argument('-n', '--num', help="number of results returned", type=int)
        parsed = parser.parse_args()
    except Exception as ex:
        print(ex)
        exit(2)
    return parsed


def main():
    warnings.filterwarnings("ignore")

    args = parsing()

    search = GrantSearch()
    if args.update:
        names = os.listdir(r"funding_opportunities")
        print(len(names))
        search.store_documents(names[0:50])

    if args.query is not None:
        if args.num is not None:
            search.search(args.query, num=args.num)
        else:
            search.search(args.query)


if __name__ == "__main__":
    main()
