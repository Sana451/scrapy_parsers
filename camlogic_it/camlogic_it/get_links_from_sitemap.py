import csv

import requests
from bs4 import BeautifulSoup

sitemap_url = "https://www.camlogic.it/sitemap.xml"

with open(
        "/home/sana451/PycharmProjects/scrapy_parsers/camlogic_it/camlogic_it/results/links.csv",
        "a") as link_file:
    soup = BeautifulSoup(requests.get(sitemap_url).content, "xml")
    links = [[loc.text] for loc in soup.select("loc") if ("/detail/" in loc.text and "/en/" in loc.text)]
    writer = csv.writer(link_file)
    writer.writerows(links)
