import csv

import requests
from bs4 import BeautifulSoup

sitemap_urls_de = ["https://shop.end.de/media/sitemap/sitemap_de-2-1.xml",
                   "https://shop.end.de/media/sitemap/sitemap_de-2-2.xml"]

with open("/home/sana451/PycharmProjects/scrapy_parsers/shop_end_de/shop_end_de/results/shop.end.de.links.csv",
          "a") as link_file:
    for map in sitemap_urls_de:
        soup = BeautifulSoup(requests.get(map).content, "xml")
        links = [[loc.text] for loc in soup.select("loc") if not loc.text.endswith(".jpg")]
        writer = csv.writer(link_file)
        writer.writerows(links)
