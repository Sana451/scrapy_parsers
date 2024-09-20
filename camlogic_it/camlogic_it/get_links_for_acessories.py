import csv

import requests
from bs4 import BeautifulSoup

url = "https://www.camlogic.it/en/accessories"

with open(
        "/home/sana451/PycharmProjects/scrapy_parsers/camlogic_it/camlogic_it/results/accesories_links.csv",
        "w") as link_file:
    soup = BeautifulSoup(requests.get(url).content)

    cats = soup.select("div.prod-item-inner a.front-cta-button")
    cats_links = [[a.attrs["href"]] for a in cats]
    for url in cats_links:
        soup = BeautifulSoup(requests.get(url).content)

        writer = csv.writer(link_file)
        writer.writerows(links)
