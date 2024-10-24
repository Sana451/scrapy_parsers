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


class BediaKabelDeSpiderSpider(scrapy.Spider):
    name = "bedia_kabel_de_spider"
    allowed_domains = ["www.bedia-kabel.de"]

    def start_requests(self):
        with open(RESULTS_DIR / "bedia-kabel.de.links.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            start_urls = [row[0] for row in list(reader)][1:]
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                )

    def parse(self, response):
        result = dict()

        DOMAIN = "http://www.bedia-kabel.de"

        result["url"] = response.url

        try:
            field = "Заголовок"
            result[field] = response.css("#bd_results h1::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            result[field] = response.xpath(
                "//td[contains(text(), 'Part Number')]//following-sibling::td//text()"
            ).get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            result[field] = response.css(".geldwert::text").get() + "." + response.css(".centwert sup::text").get()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена за 100 м."
            result[field] = response.css(".einheitspreis::text").get().replace("€", "").strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Наличие"
            result[field] = response.css(".availability::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Срок доставки"
            result[field] = response.css(".availability::text").getall()[1].strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            result[field] = DOMAIN + response.css(".main-image img").attrib["src"]
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Упаковка"
            result[field] = response.xpath(
                "//td[contains(text(), 'Packaging')]//following-sibling::td//text()"
            ).get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Вес"
            result[field] = response.xpath(
                "//td[contains(text(), 'Product Weight')]//following-sibling::td//text()"
            ).get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Характеристики"
            result[field] = my_tools.del_classes_from_html(response.css(".produktdaten table").get())
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Тех. информация"
            result[field] = "\n".join(response.css("article div.description div")[0].css("p::text").getall())
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Особенности"
            result[field] = my_tools.del_classes_from_html(
                response.css(".produktinfo table").get()
            )
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            result[field] = " > ".join([a.css("::text").get() for a in response.css("#breadcrumbs a")][2:])
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result
