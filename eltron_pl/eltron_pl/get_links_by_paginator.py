import csv
import time

from selenium.common import NoSuchElementException
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

# categories_soup = BeautifulSoup(requests.get("https://eltron.pl/").content, "html.parser")
# categories = [DOMAIN + a["href"] for a in categories_soup.select(".category-links a")]
#
#
carlo_gavazzi_subcats = [
    ("https://eltron.pl/en/szukaj=Carlo%20Gavazzi/1/6703/0", 11),
    ("https://eltron.pl/en/szukaj=Carlo%20Gavazzi/1/6747/0", 61),
    ("https://eltron.pl/en/szukaj=Carlo%20Gavazzi/1/6697/0", 3),
    ("https://eltron.pl/en/szukaj=Carlo%20Gavazzi/1/6704/0", 39),
    ("https://eltron.pl/en/szukaj=Carlo%20Gavazzi/1/7357/0", 5),
    ("https://eltron.pl/en/szukaj=Carlo%20Gavazzi/1/6707/0", 97),
    ("https://eltron.pl/en/szukaj=Carlo%20Gavazzi/1/6699/0", 224),
    ("https://eltron.pl/en/szukaj=Carlo%20Gavazzi/1/6705/0", 2)
]

all_gavazzi = "https://eltron.pl/en/szukaj=Carlo%2BGavazzi#"

all_links = []

browser = webdriver.Chrome()

for sub_cat in carlo_gavazzi_subcats[:]:
    for i in range(1, int(sub_cat[1]) + 1):
        url = sub_cat[0].split("/")
        time.sleep(5)
        url.append(f"#{i}")
        print("/".join(url))
        browser.get("/".join(url))

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
                "/home/sana451/PycharmProjects/scrapy_parsers/eltron_pl/eltron_pl/results/eltron.pl.carlo-gavazzi.links.csv",
                "a") as f:
            writer = csv.writer(f)
            for l in links:
                writer.writerow([l])
        print("Count: ", len(all_links))


# for i in range(1, 301):
#     url = all_gavazzi + str(i)
#     browser.get(url)
#     time.sleep(5)
#     WebDriverWait(browser, 5).until(
#         EC.presence_of_all_elements_located(
#             (
#                 By.CSS_SELECTOR,
#                 "h2.product-name a",
#             )
#         )
#     )
#     links = browser.find_elements(By.CSS_SELECTOR, "h2.product-name a")
#     links = [a.get_attribute("href") for a in links]
#     print(len(links))
#     all_links.extend(links)
#     with open(
#             "/home/sana451/PycharmProjects/scrapy_parsers/eltron_pl/eltron_pl/results/eltron.pl.carlo-gavazzi.links2.csv",
#             "a") as f:
#         writer = csv.writer(f)
#         for l in links:
#             writer.writerow([l])
#     print("Count: ", len(all_links))
