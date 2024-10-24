import pandas
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://shop.murrelektronik.de/sitemap_shop_1.xml")
maps_soup = BeautifulSoup(resp.content, "xml")
maps = [loc.text for loc in maps_soup.select("loc") if "/products" in loc.text]

all_urls = set()

for map in maps:
    resp = requests.get(map)
    soup = BeautifulSoup(resp.content, "xml")
    urls = [loc.text for loc in soup.select("loc")]

    all_urls.update(urls)
    print(len(all_urls))


pandas.DataFrame(all_urls).to_csv(
    "/shop_murrelektronik_de/shop_murrelektronik_de/results/shop.murrelektronik.de.links.csv",
    index=False)
