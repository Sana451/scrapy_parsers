import csv

import requests
from bs4 import BeautifulSoup

sitemap_urls_en = ["https://www.riegler.de/de/en/media/sitemap/sitemap_en-1-1.xml",
                   "https://www.riegler.de/de/en/media/sitemap/sitemap_en-1-2.xml",
                   "https://www.riegler.de/de/en/media/sitemap/sitemap_en-1-3.xml"]

sitemap_urls_de = ["https://www.riegler.de/de/de/media/sitemap/sitemap_de-2-1.xml",
                   "https://www.riegler.de/de/de/media/sitemap/sitemap_de-2-2.xml",
                   "https://www.riegler.de/de/de/media/sitemap/sitemap_de-2-3.xml"]

with open("/home/sana451/PycharmProjects/scrapy_parsers/riegler_de/riegler_de/results/rieder_links.csv",
          "a") as link_file:
    for map in sitemap_urls_de:
        soup = BeautifulSoup(requests.get(map).content, "xml")
        links = [[loc.text] for loc in soup.select("loc") if loc.text.endswith(".html")]
        writer = csv.writer(link_file)
        writer.writerows(links)
