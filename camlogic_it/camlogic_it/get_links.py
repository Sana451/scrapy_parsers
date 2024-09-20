import csv

import requests
from bs4 import BeautifulSoup

url = "https://www.camlogic.it/en/level-sensors"

with open(
        "/home/sana451/PycharmProjects/scrapy_parsers/camlogic_it/camlogic_it/results/links.csv",
        "w") as link_file:
    soup = BeautifulSoup(requests.get(url).content)
    a_tags = soup.select("div.prod-item-img a")
    links = [[a.attrs["href"]] for a in a_tags]
    writer = csv.writer(link_file)
    writer.writerows(links)
