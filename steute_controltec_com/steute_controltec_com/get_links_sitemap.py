import pandas
import requests
from bs4 import BeautifulSoup

map_urls = [
    "https://www.steute-controltec.com/de/sitemap.xml?page=1&sitemap=ofarticles&cHash=745815751c6998c62221cd60614accaa",
    "https://www.steute-controltec.com/de/sitemap.xml?page=2&sitemap=ofarticles&cHash=e06cd77bdbfbc5735c1d6b33da90237f",
    "https://www.steute-controltec.com/de/sitemap.xml?page=3&sitemap=ofarticles&cHash=31b744e748f5e49a1a35255a830f1b7c"
]

all_links = set()

for url in map_urls:
    soup = BeautifulSoup(requests.get(url).content, "xml")

    links = set(loc.text for loc in soup.select("loc"))
    print(url)
    print(len(links))
    all_links.update(links)

pandas.DataFrame(links).to_csv(
    "/steute_controltec_com/steute_controltec_com/results/steute-controltec.com.links.csv",
    index=False)
