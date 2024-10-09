import csv
import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas

DOMAIN = "https://eltron.pl"

with open("/home/sana451/PycharmProjects/scrapy_parsers/eltron_pl/eltron_pl/results/articles.carlo-gavazzi.csv", 'r') as f:
    reader = csv.reader(f)
    articles = [row[0] for row in list(reader)]

all_links = []

browser = webdriver.Chrome()

for art in articles[:]:
    url = f"https://eltron.pl/en/szukaj={art}"
    browser.get(url)
    time.sleep(5)
    try:
        WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "h2.product-name a",
                )
            )
        )
        links = browser.find_elements(By.CSS_SELECTOR, "h2.product-name a")
        links = [a.get_attribute("href") for a in links]
        print(len(links))
        all_links.extend(links)
        with open(
                "/home/sana451/PycharmProjects/scrapy_parsers/eltron_pl/eltron_pl/results/eltron.pl.carlo-gavazzi.links2.csv",
                "a") as f:
            writer = csv.writer(f)
            for l in links:
                writer.writerow([l])
        print("Count: ", len(all_links))
    except TimeoutException:
        continue

