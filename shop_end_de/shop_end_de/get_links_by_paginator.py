import csv

import requests
from bs4 import BeautifulSoup

categories = [
    # "https://shop.end.de/en/valves",
    # "https://shop.end.de/de/zubehoer",
    # "https://shop.end.de/de/verschraubungen",
    # "https://shop.end.de/de/flansche-kompensatoren",
    # "https://shop.end.de/de/neuheiten"
    # "https://shop.end.de/de/armaturen/absperrklappen/elektrisch-betaetigt",
    # "https://shop.end.de/de/armaturen/absperrklappen/ersatzteile",
    # "https://shop.end.de/de/armaturen/absperrklappen/pneumatisch-betaetigt",
    # "https://shop.end.de/de/armaturen/absperrklappen/elektrisch-betaetigt",
    # "https://shop.end.de/de/armaturen/absperrklappen/hand-betaetigt",
    # "https://shop.end.de/de/armaturen/antriebe-und-zubehoer/hubantriebe",
    # "https://shop.end.de/de/armaturen/antriebe-und-zubehoer/montagezubehoer/schalldaempfer",
]
with open("/home/sana451/PycharmProjects/scrapy_parsers/shop_end_de/shop_end_de/results/shop.de.cats.csv",
          "r") as cats_csv:
    reader = csv.reader(cats_csv)
    csv_cats = [cat[0] for cat in list(reader)]

with open("/home/sana451/PycharmProjects/scrapy_parsers/shop_end_de/shop_end_de/results/shop.end.de.links3.csv",
          "a") as csv_file:
    writer = csv.writer(csv_file)

    # for cat_url in categories[:]:
    for cat_url in csv_cats:
        try:
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
                    if len(hrefs) == 0:
                        break
                    print(len(hrefs))
                    for row in hrefs:
                        writer.writerow([row])
                    i += 1
        except Exception:
            pass
