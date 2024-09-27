import csv

import requests
import json
from bs4 import BeautifulSoup
import pandas

DOMAIN = "https://www.flixpart.de"
# CGI = "https://www.landefeld.com/cgi/main.cgi/ajax"
AJAX = "https://search.flixpart.de/indexes/products/search"


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

# with open("/home/sana451/PycharmProjects/scrapy_parsers/landefeld_com/landefeld_com/results/categories.csv") as cat_f:
#     reader = csv.reader(cat_f)
#     cat_links = list(reader)
#
# result_links = []

def get_count(brand):
    response = requests.get(url=AJAX,
                            data={"q": brand, "page": 1},
                            headers={
                                "Authorization": "Bearer 38a7037ddd94ef1415c316364be60785c02b23aa822e57d44c1e4fa587879a73"
                            })


result = set()

i = 1

while True:
    data = {"q": "STAUFF", "page": i}
    response = requests.get(url=AJAX,
                            params=data,
                            headers={
                                "Authorization": "Bearer 38a7037ddd94ef1415c316364be60785c02b23aa822e57d44c1e4fa587879a73"
                            }
                            )

    if response.json()["hits"]:
        hits = [i for i in response.json()["hits"]]
        slugs = [hit["handle"] for hit in hits]
        urls = [f"{DOMAIN}/{slug}" for slug in slugs]
        result.update(urls)
        i += 1
    else:
        break
    # product_count = int(response.json()["Anzahl_Artikel_gesamt"])

#     print(result_links)
#     print(len(result_links))
#     # with open("/home/sana451/PycharmProjects/scrapy_parsers/landefeld_com/landefeld_com/results/categories_links/ladefeld_all_product_urls.csv", "a") as res_file:
#     #     writer = csv.writer(res_file)
#
#     for chank in range(0, product_count + 20, 20):
#         data["param_1"] = chank
#         response = requests.get(CGI, data=data)
#         soup = BeautifulSoup(response.json()["html"])
#
#         for a in soup.select("a"):
#             url = f"{DOMAIN}{a['href']}".replace("/de/", "/en/")
#             result_links.append(
#                 [url, cat_link[0]]
#             )
#             # print(result_links)
pandas.DataFrame(result).drop_duplicates().to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/flixpart_de/flixpart_de/results/links.stauff.flixpart.de.csv",
    index=False)
