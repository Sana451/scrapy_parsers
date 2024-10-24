import pandas
import requests
from bs4 import BeautifulSoup

cats = [
    "https://www.zetasassi.com/LINEAR-AUTOMATIC-TENSIONERS",
    "https://www.zetasassi.com/ROTARY-AUTOMATIC-ARM-TENSIONERS",
    "https://www.zetasassi.com/DIRECTABLE-TENSIONERS",
    "https://www.zetasassi.com/ADJUSTABLE-TENSIONERS",
    "https://www.zetasassi.com/CHAIN-SLIDER-TENSIONER",
    "https://www.zetasassi.com/IDLER-ROLLERS",
    "https://www.zetasassi.com/TRAPEZOIDAL-WHARVES-PULLEYS",
    "https://www.zetasassi.com/IDLER-SPROCKETS",
    "https://www.zetasassi.com/TORQUE-LIMITER",
    "https://www.zetasassi.com/AXIAL-POWER-LIMITERS",
    "https://www.zetasassi.com/ADJUSTABLE-CAMS",
    "https://www.zetasassi.com/AUTOMATIC-GREASERS",
    "https://www.zetasassi.com/ERGAL-SCREWS",
]

all_links = set()

for cat_url in cats[:]:
    url = cat_url
    print("\n", cat_url, "\n")
    page_num = 1
    while True:
        print("Page: ", page_num)
        resp = requests.get(cat_url, params={"page": page_num})
        if resp.history and resp.history[0].status_code == 301:
            print(f"Not found links {cat_url} {page_num}")
            break
        soup = BeautifulSoup(resp.content, "html.parser")
        links = soup.select(".products .name a")

        links = ["https://www.zetasassi.com" + a["href"] for a in links]
        all_links.update(links)
        print(len(all_links))
        page_num += 1

pandas.DataFrame(all_links).to_csv(
    path_or_buf="/home/sana451/PycharmProjects/scrapy_parsers/zetasassi_com/zetasassi_com/results/zetasassi.com.links.csv",
    index=False)
