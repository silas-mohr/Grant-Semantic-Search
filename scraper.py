import unicodedata
import requests
import re
import csv
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

# document_numbers = ["PAR-23-110", "PAR-18-604", "PAR-21-133", "PAR-21-143"]
# # # document_numbers = ["RFA-MH-21-180"]
# for document_number in document_numbers:
#     print(document_number)
#     URL = f"https://grants.nih.gov/grants/guide/pa-files/{document_number}.html"
#     # URL = f"https://grants.nih.gov/grants/guide/rfa-files/{document_number}.html"
#
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, "html.parser")
#
#     purpose = soup.find("div",
#                         class_="col-md-4 datalabel",
#                         string=lambda text: (
#                                     "Funding Opportunity Purpose" in text.strip()) if text is not None else text)
#     purpose = purpose.find_next_sibling().text
#     purpose = unicodedata.normalize('NFKD', purpose).replace('\n', ' ').replace('\r', ' ').lower().strip()
#     purpose = re.sub(' +', ' ', purpose)
#
#     description_tag = soup.select_one('a[name="_Section_I._Funding"]')
#     description = ""
#     while True:
#         description_tag = description_tag.find_next()
#         desc_para = unicodedata.normalize('NFKD', description_tag.text).replace('\n', ' ').replace('\r', ' ').lower().strip()
#         desc_para = re.sub(' +', ' ', desc_para)
#         if desc_para == 'see section viii. other information for award authorities and regulations.':
#             break
#         description += desc_para + " "
#
#     funding_opportunity = {
#         'document_number': document_number,
#         'purpose': purpose,
#         'description': description
#     }


# class GrantScraper:
#     def __init__(self, file_path: str):
#         self.file_path = file_path
#
#     def read_file(self) -> list:
#         output = []
#         with open(self.file_path, "r") as f:
#             reader = csv.reader(f)
#             for i in range(1300):
#                 next(reader)
#             for line in reader:
#                 output.append({'title': line[0], 'document_number': line[7], 'url': line[10]})
#         return output
#
#     def scrape(self):
#         output = []
#         documents = self.read_file()
#         for document in documents:
#             page = requests.get(document['url'])
#             soup = BeautifulSoup(page.content, "html.parser")
#             purpose = soup.find("div",
#                                 class_="col-md-4 datalabel",
#                                 string=lambda text: (
#                                         "Funding Opportunity Purpose" in text.strip()) if text is not None else text)
#             purpose = purpose.find_next_sibling().text
#             purpose = unicodedata.normalize('NFKD', purpose).replace('\n', ' ').replace('\r', ' ').lower().strip()
#             purpose = re.sub(' +', ' ', purpose)
#
#             description_tag = soup.select_one('a[name="_Section_I._Funding"]')
#             description = ""
#             while True:
#                 description_tag = description_tag.find_next()
#                 desc_para = unicodedata.normalize('NFKD', description_tag.text).replace('\n', ' ').replace('\r', ' ').lower().strip()
#                 desc_para = re.sub(' +', ' ', desc_para)
#                 if desc_para == 'see section viii. other information for award authorities and regulations.':
#                     break
#                 description += desc_para + " "
#             funding_opportunity = {
#                 "title": document["title"],
#                 "document_number": document["document_number"],
#                 "purpose": purpose,
#                 "description": description
#             }
#             output.append(funding_opportunity)

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
                    "text": text
                }
                output.append(funding_opportunity)
                with open("./funding_opportunities/" + doc["document_number"] + ".txt", 'w', encoding="utf-8") as f:
                    f.write(f'{doc["title"]}\n')
                    f.write(f"{text}")
            except Exception as ex:
                print(doc["document_number"])
                print(ex)


def main():
    scraper = GrantScraper('datasets/active_funding.csv')
    print(scraper.scrape())


if __name__ == "__main__":
    main()
