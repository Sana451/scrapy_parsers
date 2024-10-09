import csv

import requests
from bs4 import BeautifulSoup

sitemap_url = "https://www.schmalz.com/de-de/sitemap-products.xml"

with open("/home/sana451/PycharmProjects/scrapy_parsers/schmalz_com/schmalz_com/results/schmalz.com.links.csv",
          "a") as link_file:
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, "xml")
    links = [[loc.text] for loc in soup.select("loc")]
    writer = csv.writer(link_file)
    writer.writerows(links)
