import pandas
import requests
from bs4 import BeautifulSoup

map_url = "https://www.ace-ace.de/media/sitemap/sitemap_de.xml"

soup = BeautifulSoup(requests.get(map_url).content, "xml")

links = set(
    [
        loc.text for loc in soup.select("loc") if
        (".html" in loc.text
         and "accessories/" not in loc.text
         and "/news-presse/" not in loc.text
         and "/knowledge-base" not in loc.text
         and "/glossary-of" not in loc.text
         and "/lp/" not in loc.text
         and "/anwendungen/" not in loc.text
         and "/berechnungen/" not in loc.text
         and "/service-downloads/" not in loc.text
         and "/unternehmen/" not in loc.text
         and "/vertrieb-kontakt/" not in loc.text
         )
    ]
)

print(len(links))

pandas.DataFrame(links).to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/ace_ace_de/ace_ace_de/results/ace-ace.de.links.csv",
    index=False)
