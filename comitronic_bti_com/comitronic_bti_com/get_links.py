import requests
from bs4 import BeautifulSoup
import pandas

CATALOG_URL = "https://www.comitronic-bti.de/de/katalog"
DOMAIN = "https://www.comitronic-bti.de"


def crawl_catalog(url):
    category_urls = set([url])
    product_urls = set()
    while category_urls:
        url = category_urls.pop()
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        for a in soup.select(".grid a"):
            if "/produkt/" in a["href"]:
                product_urls.add(f"{DOMAIN}{a['href']}")
            else:
                category_urls.add(f"{DOMAIN}{a['href']}")

    print(product_urls)
    print(len(product_urls))
    print("Cat urls", len(category_urls))
    pandas.DataFrame(
        product_urls).to_csv(
        "/home/sana451/PycharmProjects/scrapy_parsers/comitronic_bti_com/comitronic_bti_com/results/comitronic-bti.de.cats.csv",
    index=False)


crawl_catalog(CATALOG_URL)
