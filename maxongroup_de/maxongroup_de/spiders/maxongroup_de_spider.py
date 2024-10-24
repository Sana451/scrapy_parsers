import csv
import json
import sys
import time
from typing import Iterable

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
browser.implicitly_wait(5)
browser.maximize_window()
browser.get("https://www.maxongroup.de/maxon/view/product/motor/ecmotor/ecframeless/EC50Frameless/734439")
time.sleep(5)


class MaxongroupDeSpiderSpider(scrapy.Spider):
    name = "maxongroup_de_spider"
    allowed_domains = ["maxongroup.de"]

    def start_requests(self):
        with open(RESULTS_DIR / "maxogroup.de.links.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            start_urls = [row[0] for row in list(reader)][1:]
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                )

    def parse(self, response):
        result = dict()

        DOMAIN = "https://www.maxongroup.de"

        result["url"] = response.url

        try:
            field = "Загловок"
            result[field] = response.css("h1.name::text").get().strip(" |").strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Marketing text"
            result[field] = response.css(".marketingText::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            result[field] = response.css(".articleNumber::text").get().replace("Artikelnummer", "").strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            result[field] = response.css(
                "table.articlePriceRanges tbody td::text"
            )[2].get().replace("€", "").replace("'", ".").strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Кол-во (к цене)"
            result[field] = response.css("table.articlePriceRanges tbody td::text")[1].get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Наличие"
            browser.get(response.url)
            time.sleep(3)
            browser.find_element(By.CSS_SELECTOR, ".orderInput .button").click()
            time.sleep(3)
            browser.find_element(By.XPATH, "//a[contains(text(), 'Zum War')]").click()
            time.sleep(3)
            availabillity_state_class = browser.find_element(
                By.CSS_SELECTOR, "span.article-delivery-state__indicator").get_attribute("class").split()[-1]
            time.sleep(3)
            if availabillity_state_class == "article-delivery-state__deliveryInfo":
                result[field] = "Niedrig"
            elif availabillity_state_class == "article-delivery-state__withinNextDays":
                result[
                    field] = "Mittel"
            elif availabillity_state_class == "article-delivery-state__available":
                result[field] = "Hoch"
            else:
                result[field] = ""

            browser.find_element(By.XPATH, "//*[contains(text(), 'Entfernen')]").click()

        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            "article-delivery-state__deliveryInfo" "В настоящее время этого продукта нет на складе."
            "article-delivery-state__withinNextDays" "Продукта нет на складе, но компоненты доступны. Мы изготовим и доставим вам не более 10 штук в течение 11 рабочих дней (срок поставки до 15 рабочих дней). "
            "article-delivery-state__available" "Этот продукт находится на основном складе и отправляется в течение 24 часов в рабочие дни. Срок поставки: около 2-5 рабочих дней"

        try:
            field = "Картинки"
            result[field] = "https://www.maxongroup.de" + response.css(".articleImage img").attrib["src"]
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "PDF"
            result[field] = "https://www.maxongroup.de" + response.xpath("//a[contains(text(), 'deutsch')]")[0].attrib[
                'href']
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Описание"
            result[field] = response.css(".tabDescription span::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Технические характеристики"
            table = response.css(".iTabSpecifications table").get()
            if table != '<table>\r\n                </table>':
                result[field] = my_tools.del_classes_from_html(table)
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            result[field] = " > ".join(response.url.split("/")[6:-1])
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result

