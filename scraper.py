import unicodedata
import requests
import re
import csv
from bs4 import BeautifulSoup
import os
from tqdm import tqdm


class GrantScraper:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file(self) -> list:
        output = []
        with open(self.file_path, "r") as f:
            reader = csv.reader(f)
            for i in range(1000):
                next(reader)
            for line in reader:
                output.append({'title': line[0], 'document_number': line[7], 'url': line[10]})
        return output

    def scrape(self):
        output_folder = os.path.join(os.getcwd(), r'funding_opportunities')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output = []
        documents = self.read_file()
        for doc in tqdm(documents):
            try:
                page = requests.get(doc['url'])
                soup = BeautifulSoup(page.content, "html.parser")
                paragraphs = soup.find_all('p')
                text = ""
                for paragraph in paragraphs:
                    text += paragraph.get_text()
                    try:
                        text = unicodedata.normalize('NFKD', text).replace('\n', ' ').replace('\r', ' ').lower().strip()
                    except Exception as ex:
                        print(f"Exception normalizing the text: {ex}")
                    text = re.sub(r'\s+', ' ', text)
                funding_opportunity = {
                    "title": doc["title"],
                    "document_number": doc["document_number"],
                    "URL": doc["url"],
                    "text": text
                }
                output.append(funding_opportunity)
                with open("./funding_opportunities/" + doc["document_number"] + ".txt", 'w', encoding="utf-8") as f:
                    f.write(f'{doc["title"]}\n')
                    f.write(f'{doc["url"]}\n')
                    f.write(f"{text}")
            except Exception as ex:
                print(doc["document_number"])
                print(ex)


def main():
    scraper = GrantScraper('datasets/active_funding.csv')
    print(scraper.scrape())


if __name__ == "__main__":
    main()
