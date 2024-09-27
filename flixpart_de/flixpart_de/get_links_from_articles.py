import csv

import requests
import json
from bs4 import BeautifulSoup
import pandas

DOMAIN = "https://www.flixpart.de"

with open("/home/sana451/PycharmProjects/scrapy_parsers/flixpart_de/flixpart_de/results/stauff.atricles.csv",
          "r") as csv_file:
    reader = csv.reader(csv_file)
    articles = [column[1] for column in list(reader)]

result = set()

# for article in articles:
for article in ["1020023861"]:
    response = requests.get(url=f"https://www.flixpart.de/q?query={article}",
                            headers={
                                "Authorization": "Bearer 38a7037ddd94ef1415c316364be60785c02b23aa822e57d44c1e4fa587879a73"
                                ,
                                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"},
                            proxies={
                                'http': 'http://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
                                # 'https': 'https://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
                            },
                            )

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
