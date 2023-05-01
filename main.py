import os
import random
import warnings
import argparse as ap
from tqdm import tqdm
import time
import numpy as np
import matplotlib.pyplot as plt

from grant_search import GrantSearch


def parsing():
    try:
        parser = ap.ArgumentParser(description='Semantic Search for Government Grants Within Healthcare', allow_abbrev=False)
        parser.add_argument('update', help='should the document store be updated?', type=int)
        parser.add_argument('-n', '--num', help="number of iterations to average over", type=int)
        parsed = parser.parse_args()
    except Exception as ex:
        print(ex)
        exit(2)
    return parsed


def main():
    warnings.filterwarnings("ignore")  # Prevents warning about TypedStorage that doesn't affect this program

    args = parsing()
    num_iterations = args.num
    average_times = []
    seed = 10

    search = GrantSearch()
    if args.update:
        names = os.listdir(r"funding_opportunities")
        print(len(names))
        # search.store_documents(names)

    queries = ["Where can I find funding to study alcoholism?",
               "Where can I find funding to study alcoholism and alcohol abuse?",
               "Where is funding for studying alcoholism?",
               "Where is funding for studying alcoholism and alcohol abuse?",
               "Where can I find funding to study cancer?",
               "Where can I find funding to study lung disease?",
               "Where is funding to study lung disease?",
               "Where is funding to study cancer?",
               "Where can I find funding to study the long term effects of covid-19?",
               "alcoholism",
               "alcoholism and alcohol abuse",
               "cancer",
               "lung disease",
               "covid",
               "covid-19"
               ]

    num_results = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    np.random.seed(seed)

    for i in range(num_iterations):
        times = []
        for num in num_results:  # tqdm(num_results, bar_format='{l_bar}{bar:30}{r_bar}'):
            query = queries[random.randint(0, len(queries) - 1)]
            start = time.perf_counter()
            search.search(query, num=num, print_results=False)
            total_time = time.perf_counter() - start
            times.append(total_time)
        print(f"Finished round {i+1}")
        average_times.append(times)
    average_times = np.mean(average_times, axis=0)

    plt.plot(num_results, average_times, 'r', label="data")

    plt.xlabel("Number of results")
    plt.ylabel("Time (s)")
    plt.title("Search Time By Number of Results")
    plt.legend(["Runtime"])
    plt.show()


if __name__ == "__main__":
    main()
