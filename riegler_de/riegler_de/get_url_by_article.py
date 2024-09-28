import csv

import requests

with open("/home/sana451/PycharmProjects/scrapy_parsers/riegler_de/riegler_de/results/articles.riegler.csv",
          "r") as article_csv:
    reader = csv.reader(article_csv)
    articles = [a[0] for a in list(reader)]

# print(articles)
# print(len(articles))


with open("/home/sana451/PycharmProjects/scrapy_parsers/riegler_de/riegler_de/results/riegler_links2.csv",
          "w") as links_csv:
    writer = csv.writer(links_csv)

    for art in articles:
        resp = requests.get("https://www.riegler.de/de/de/search/ajax/suggest", params={"q": art})
        res = resp.json()
        urls = [res_element.get("url") for res_element in res]
        for url in urls:
            print(art, url)
            writer.writerow([url])
