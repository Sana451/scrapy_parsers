import pandas
import requests
from bs4 import BeautifulSoup

DOMAIN = "http://www.bedia-kabel.de"

urls = ["http://www.bedia-kabel.de/en/webshop/products-en.html?limit=701&start=1",
        "http://www.bedia-kabel.de/en/webshop/products-en.html?limit=701&start=701",
        "http://www.bedia-kabel.de/en/webshop/products-en.html?limit=701&start=1402"]

all_links = []

for url in urls:
    resp = requests.get(url)

    soup = BeautifulSoup(resp.content, "html.parser")

    links = [DOMAIN + a["href"] for a in soup.select("div.product h2 a")]
    print(len(links))
    all_links.extend(links)


print(len(all_links))

pandas.DataFrame(all_links, columns=["url", ]).to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/bedia_kabel_de/bedia_kabel_de/results/bedia-kabel.de.links.csv",
    index=False)
