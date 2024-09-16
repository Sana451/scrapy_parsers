import csv

import requests
import json
from bs4 import BeautifulSoup
import pandas

DOMAIN = "https://www.landefeld.com"
CGI = "https://www.landefeld.com/cgi/main.cgi/ajax"

# links = []
# for i in range(0, 860, 20):
#     data = {"DISPLAY": "artikelgruppe_nachladen", "param_0": "_IMI", "param_1": i}
#     response = requests.get(CGI, data=data)
#     soup = BeautifulSoup(response.json()["html"])
#
#     for a in soup.select("a"):
#         url = f"{DOMAIN}{a['href']}".replace("/de/", "/en/")
#         links.append(url)
#
# pandas.DataFrame(links).drop_duplicates().to_csv(
#     "/home/sana451/PycharmProjects/scrapy_parsers/landefeld_com/landefeld_com/results/categories_links/cat1.csv",
#     index=False)

with open("/home/sana451/PycharmProjects/scrapy_parsers/landefeld_com/landefeld_com/results/categories.csv") as cat_f:
    reader = csv.reader(cat_f)
    cat_links = list(reader)

result_links = []

for cat_link in cat_links:
    param_o = cat_link[0].split("/")[-1]

    data = {"DISPLAY": "artikelgruppe_nachladen", "param_0": param_o, "param_1": ""}

    response = requests.get(CGI, data=data)
    product_count = int(response.json()["Anzahl_Artikel_gesamt"])

    print(result_links)
    print(len(result_links))
    # with open("/home/sana451/PycharmProjects/scrapy_parsers/landefeld_com/landefeld_com/results/categories_links/ladefeld_all_product_urls.csv", "a") as res_file:
    #     writer = csv.writer(res_file)

    for chank in range(0, product_count + 20, 20):
        data["param_1"] = chank
        response = requests.get(CGI, data=data)
        soup = BeautifulSoup(response.json()["html"])

        for a in soup.select("a"):
            url = f"{DOMAIN}{a['href']}".replace("/de/", "/en/")
            result_links.append(
                [url, cat_link[0]]
            )
            # print(result_links)
pandas.DataFrame(result_links).drop_duplicates().to_csv(
    "/landefeld_com/landefeld_com/results/categories_links/ladefeld_all_product_urls.csv",
    index=False)
