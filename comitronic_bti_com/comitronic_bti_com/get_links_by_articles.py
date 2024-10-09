import csv

import pandas
from selenium import webdriver
from bs4 import BeautifulSoup

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

with open(
        "/home/sana451/PycharmProjects/scrapy_parsers/comitronic_bti_com/comitronic_bti_com/results/comitronic-bti.de.articles.csv",
        mode="r", encoding="utf-8") as articles_csv_file:
    reader = csv.reader(articles_csv_file)
    articles = [row[0] for row in list(reader)][1:]

result = set()
browser = webdriver.Chrome()
browser.get("https://www.comitronic-bti.de/de/recherche")
for art in articles[:]:
    input = browser.find_element(By.ID, "front_recherche__rech")
    input.clear()
    input.send_keys(art)
    input.send_keys(Keys.ENTER)
    links = browser.find_elements(By.CSS_SELECTOR, "a.w-full")
    links = [l.get_attribute("href") for l in links]
    result.update(links)
    print(len(links))

print("Count", len(result))
pandas.DataFrame(result).to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/comitronic_bti_com/comitronic_bti_com/results/comitronic-bti.de.arts.csv",
    index=False)
