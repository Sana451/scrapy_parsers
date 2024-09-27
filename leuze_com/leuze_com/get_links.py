import csv
import re
import sys

sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
import requests
from bs4 import BeautifulSoup

from tools.my_scraping_tools import cookie_dict_from_string

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"}
cookies = cookie_dict_from_string("session-=c2ahqupqrnnaotnprrchdog2r9")

response = requests.get("https://www.leuze.com/en-int/sitemap.xml",
                        headers=headers,
                        # cookies=cookies
                        )

soup = BeautifulSoup(response.content, "xml")

sitemaps = [loc.text for loc in soup.select("sitemap loc")]

result_links = 0

with open("/home/sana451/PycharmProjects/scrapy_parsers/leuze_com/leuze_com/results/links.csv", "w", newline="",
          encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)

    for map_url in sitemaps:
        print("\nSitemap: ", map_url, "\n\n")
        response = requests.get(map_url, headers=headers)
        soup = BeautifulSoup(response.content, "xml")
        locs = soup.select("loc")
        pattern = re.compile(r"http[s]?://www.leuze.com/en-int/.+/\d+")
        product_links = [link.text for link in locs if pattern.fullmatch(link.text)]
        print(f"Found {len(product_links)} products")
        result_links += len(product_links)

        for pr_link in product_links:
            writer.writerow([pr_link.replace("/en-int/", "/en-uk/")])

print(f"\nFound {result_links} products from all sitemaps")
print("Finish")
