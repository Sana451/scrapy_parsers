import csv

import requests
from bs4 import BeautifulSoup

sitemap_url = "https://www.comitronic-bti.de/de/sitemap.xml"

with open(
        "/home/sana451/PycharmProjects/scrapy_parsers/comitronic_bti_com/comitronic_bti_com/results/comitronic-bti.de.links.map.csv",
        "a") as link_file:
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, "xml")
    links = [[loc.text] for loc in soup.select("loc") if "/produkt/" in loc.text]
    writer = csv.writer(link_file)
    writer.writerows(links)
