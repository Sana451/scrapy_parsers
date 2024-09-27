import csv

import requests
from bs4 import BeautifulSoup

sitemap_1 = "https://www.bihl-wiedemann.de/de/sitemap-type/product/sitemap.xml"
sitemap_2 = "https://www.bihl-wiedemann.de/de/sitemap-type/product/page-1/sitemap.xml"

with open(
        "/home/sana451/PycharmProjects/scrapy_parsers/bihl_wiedemann_de/bihl_wiedemann_de/results/links_de.csv",
        "w") as link_file:
    for map in sitemap_1, sitemap_2:
        soup = BeautifulSoup(requests.get(map).content, "xml")
        links = [[loc.text] for loc in soup.select("loc")]
        writer = csv.writer(link_file)
        writer.writerows(links)
