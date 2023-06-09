import os
from os import name
import warnings
from sys import exit, stderr
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from pickle import dump, load
import argparse as ap
from typing import Optional

from grant_search import GrantSearch
from scraper import GrantScraper


def parsing():
    try:
        parser = ap.ArgumentParser(description='Server for the semantic search application', allow_abbrev=False)
        parser.add_argument('port', help='the port at which the server should listen', type=int)
        parser.add_argument('-u', '--update', help='1 to update the document embeddings, anything else to do nothing', type=int)
        parser.add_argument('-p', '--print', help='1 to print the results of a query, anything else to do nothing', type=int)
        parsed = parser.parse_args()
    except Exception as ex:
        print(ex, file=stderr)
        exit(2)
    return parsed


def format_list_items(documents):
    items = []
    for i, grant in enumerate(documents["documents"]):
        grant_meta = grant.meta
        name = grant_meta["name"]
        url = grant_meta["url"]
        col1 = f'{grant_meta["grant_num"]}'
        col2 = f'{url}'
        col3 = f'{name}'
        item_str = [col1, col2, col3]
        items.append(item_str)
    return items


def handle_client(sock: socket, search: GrantSearch, print_results: Optional[bool] = True):
    try:
        in_flo = sock.makefile(mode='rb')
        client_query = load(in_flo)
        print("Received command: run_query")
        if client_query.get_query():
            docs = search.search(client_query.get_query(), num=client_query.get_num(), print_results=print_results)
            response = format_list_items(docs)
            handled = True
        else:
            response = None
            handled = True
    except Exception as ex:
        response = ex
        print(ex, file=stderr)
        handled = False

    out_flo = sock.makefile(mode='wb')
    dump([handled, response], out_flo)
    out_flo.flush()


def main():
    warnings.filterwarnings("ignore")  # Prevents warning about TypedStorage that doesn't affect this program
    args = parsing()

    try:
        grant_search = GrantSearch()
        if args.update == 1:
            print("Updating document store, this can take a very long time (3-4 hours for all documents).")
            print("Re-scraping grant pages")
            scraper = GrantScraper('datasets/active_funding.csv')
            scraper.scrape()
            names = os.listdir(r"funding_opportunities")
            print(f"Found {len(names)} documents")
            grant_search.store_documents(names)
        port = args.port
        server_sock = socket()
        print('Opened server socket')
        if name != 'nt':
            server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_sock.bind(('', port))
        print('Bound server socket to port')
        server_sock.listen()
        print('Listening')
        while True:
            try:
                sock, client_addr = server_sock.accept()
                with sock:
                    print('Accepted connection, opened socket')
                    print("Client address: " + client_addr[0])
                    handle_client(sock, grant_search, print_results=(args.print == 1))
                    print("Closed socket")
            except Exception as ex:
                print(ex, file=stderr)
                exit(1)

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
