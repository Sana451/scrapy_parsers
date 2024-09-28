import csv

import requests
from bs4 import BeautifulSoup

("https://shop.end.de/de/armaturen/ed620432%20"
 "https://shop.end.de/en/valves/ed620432")

categories = [
    "https://shop.end.de/en/valves",
    "https://shop.end.de/de/zubehoer",
    "https://shop.end.de/de/verschraubungen",
    "https://shop.end.de/de/flansche-kompensatoren",
    "https://shop.end.de/de/neuheiten"
]

with open("/home/sana451/PycharmProjects/scrapy_parsers/shop_end_de/shop_end_de/results/shop.end.de.links2.csv", "w") as csv_file:
    writer = csv.writer(csv_file)

    for cat_url in categories[:]:
        i = 1
        while True:
            resp = requests.get(url=cat_url, params={"p": i, "product_list_limit": 72})
            print(f"Page {i}", cat_url)
            if "wir keine passenden Produkte" in str(resp.content) or "find products matching" in str(resp.content):
                print("End of category!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                break
            else:
                soup = BeautifulSoup(resp.content, "html.parser")
                links = soup.select("a.product")
                hrefs = [a["href"].replace("/en/valves/", "/de/armaturen/") for a in links]
                print(len(hrefs))
                for row in hrefs:
                    writer.writerow([row])
                i += 1
