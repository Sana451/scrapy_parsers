import csv
import json
import sys
import time
from selenium.webdriver.support import expected_conditions as EC

import requests
from selenium import webdriver
from scrapy import Request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from tabulate import tabulate

if sys.platform == "linux":
    sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
elif sys.platform == "win32":
    sys.path.insert(0, r"D:\sana451\scrapy_parsers")
from tools import my_scraping_tools as my_tools
from bs4 import BeautifulSoup

from pathlib import Path

import scrapy

BASE_DIR = Path("__file__").resolve().parent
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"

options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
browser = webdriver.Chrome(options=options)
browser.get("https://www.balluff.com/de-de/products/BCC032H?pf=G1102&pm=S-BCC%20SE%20SCU")
browser.maximize_window()

try:
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Allem zustimmen')]"))
    )
    button = browser.find_element(By.XPATH, "//*[contains(text(), 'Allem zustimmen')]")
    browser.execute_script("arguments[0].click();", button)
    print('Приняли куки')
    time.sleep(3)
except Exception as e:
    print(f"Ошибка клика по кнопке: {e}")


class BalluffComSpiderSpider(scrapy.Spider):
    name = "balluff_com_spider"
    allowed_domains = ["balluff.com"]

    def start_requests(self):
        with open(RESULTS_DIR / "balluff.com.links3.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            start_urls = [row[0] for row in list(reader)]
            for url in start_urls[507:]:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    # meta={"playwright": True},
                )

    def parse(self, response):

        result = dict()
        result["url"] = response.url

        try:
            js = response.xpath("//script[@type='application/ld+json']//text()").get()
            js_dict = json.loads(js)
        except Exception as error:
            my_tools.save_error(response.url, error, "JS script", ERRORS_FILENAME)

        try:
            field = "Заголовок"
            title = js_dict.get("name", "").strip()
            if not title:
                title = response.css("article h1::text").get().strip()
            result[field] = title
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Подкатегория"
            result[field] = response.css("article h2::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Код типа"
            result[field] = js_dict.get("alternateName", "")
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "SKU"
            result[field] = js_dict.get("sku", "")
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "MPN"
            result[field] = js_dict.get("mpn", "")
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            result[field] = js_dict.get("offers", "").get("price")
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        browser.get(response.url)

        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="top-price"]/div/div/div[2]/button'))
            )
            button = browser.find_element(By.XPATH, '//*[@id="top-price"]/div/div/div[2]/button')
            browser.execute_script("arguments[0].click();", button)
            time.sleep(3)
        except Exception as e:
            print(f"Ошибка клика по кнопке 'Daten abfragen': {e}")

        try:
            field = "Наличие"
            result[field] = browser.find_element(
                By.XPATH, "//p[contains(text(), 'Verfügbarkeit')]/parent::div/following-sibling::*"
            ).text.strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            result[field] = js_dict.get("image", "").replace("\\", "")
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "PDF"
            result[field] = browser.find_element(
                By.XPATH, "//a[contains(@onclick,'window.send')]"
            ).get_attribute("href")
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Описание"
            desc = browser.find_elements(By.CSS_SELECTOR, "div.leading-tightest div")
            table = []
            for i in range(0, len(desc), 2):
                table.append((desc[i].text, desc[i + 1].text))
            result[field] = tabulate(table, tablefmt="html")
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            WebDriverWait(browser, 5).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[contains(@class, 'order-2')]")
                )
            )
            cats = browser.find_elements(By.XPATH, "//a[contains(@class, 'order-2')]")
            result[field] = " > ".join(
                [a.text for a in cats][2:-1]
            )
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        # browser.quit()
        # browser = None

        yield result

# На странице товара куча ссылок (возможно на товары или модификации) "//a[@x-data]"
# //img[contains(@src, 'arrow_right')]
