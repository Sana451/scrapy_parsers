# "//*[contains(text(), 'No products found')]"
import pandas
import requests
from bs4 import BeautifulSoup

all_links = set()

for page_num in range(1, 43):
    url = f"https://ac-motoren.shop/en/Products/?b2bListingView=listing&order=name-asc&p={page_num}"
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content)
    links = [a["href"] for a in soup.select("a.product-name")]
    all_links.update(links)

    print(f"Page #{page_num}")
    print(len(all_links))

pandas.DataFrame(all_links).to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/ac_motoren_shop/ac_motoren_shop/results/ac-motoren.shop.links.csv",
    index=False)
