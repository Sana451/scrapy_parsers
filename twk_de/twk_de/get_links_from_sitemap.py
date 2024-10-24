import pandas
from bs4 import BeautifulSoup

with open("/home/sana451/PycharmProjects/scrapy_parsers/twk_de/twk_de/results/sitemap-1.xml") as f:
    soup = BeautifulSoup(f.read(), 'xml')
    links = soup.select("loc")

pandas.DataFrame(links).to_csv("/twk_de/twk_de/results/twk.de.links.csv",
                               index=False)
