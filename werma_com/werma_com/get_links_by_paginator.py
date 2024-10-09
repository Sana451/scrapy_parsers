import requests
from bs4 import BeautifulSoup
import pandas

DOMAIN = "https://www.werma.com"

categories = [
    "https://www.werma.com/en/s_c1000i/Signal_Towers/",
    "https://www.werma.com/en/s_c1004i/Systems_for_optimising_production_and_logistics_areas/",
    "https://www.werma.com/en/s_c1001i/Signal_Beacons_and_Traffic_Lights/",
    "https://www.werma.com/en/s_c1003i/Horns_and_Sirens/",
    "https://www.werma.com/en/s_c1002i/Visual_acoustic_combinations/",
]

all_links = []

for cat_url in categories[:]:
    offset = 0
    while True:
        resp = requests.get(cat_url, params={"offset": offset})
        print(resp.status_code)
        soup = BeautifulSoup(resp.content, "html.parser")
        links = [DOMAIN + a["href"] for a in soup.select("a.easy.more") if a["href"].endswith(".html")]
        all_links.extend(links)
        print(links)
        print(len(links))
        if links:
            offset += 20
        else:
            break

print(len(all_links))

pandas.DataFrame(all_links, columns=["url"]).to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/werma_com/werma_com/results/werma.com.links.csv",
    index=False)
