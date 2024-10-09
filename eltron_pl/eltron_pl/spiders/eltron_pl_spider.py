import csv
import json
import sys

import requests
from scrapy import Request
from tabulate import tabulate

sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
from tools import my_scraping_tools as my_tools
from bs4 import BeautifulSoup

from pathlib import Path

import scrapy

BASE_DIR = Path("__file__").resolve().parent
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"

cookies = {
    "site_lang": "1%2Cen_EN",
    "currency": "eur",
    "price_type": "n",
    "visit": "3359f7140edfc3db2c513e443980a2632875cace4c8c025ce847d7364cfca8d565254046",
    "CookieConsent": "{stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:1%2Cutc:1728367344250%2Cregion:%27RU%27}",
    "_gcl_au": "1.1.1944580162.1728367344",
    "304cdde60c45d96ab942c1f7dced67e0d2d3f306": "faqqcmnj8egug9fm1atgblioa2"
}


class EltronPlSpiderSpider(scrapy.Spider):
    name = "eltron_pl_spider"
    allowed_domains = ["eltron.pl"]

    def start_requests(self):
        with open(RESULTS_DIR / "eltron.pl.carlo-gavazzi.links2.csv") as f:
            reader = csv.reader(f)
            start_urls = [row[0] for row in list(reader)]
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    cookies=cookies
                )

    def parse(self, response):
        result = dict()
        result["url"] = response.url

        try:
            field = "Заголовок"
            result[field] = response.css("h1.product-title b::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            result[field] = response.css("#product_name::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Eltron code"
            result[field] = response.css("#product_id::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Производитель"
            result[field] = response.css("#product_producer a::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            result[field] = response.xpath(
                "//*[contains(@class, 'no-gutters product-price')][1]//div[2]//text()"
            ).get().strip().replace("€", "")
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "За количество"
            result[field] = response.xpath(
                "//*[contains(@class, 'no-gutters product-price')][1]//div[1]//text()"
            ).get().strip().replace("+", "")
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Наличие"
            result[field] = response.xpath("//*[@class='product-cart-section']/div[1]/text()").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Время доставки"
            result[field] = response.xpath(
                "//*[contains(@class, 'delivery-icon')]/following-sibling::*/text()").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Количество (доставка)"
            result[field] = response.xpath(
                "//*[contains(text(), 'Amount')][1]/following-sibling::div[2]/text()").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            result[field] = "https://eltron.pl" + response.css("img.img-fluid").attrib["src"]
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "PDF"
            result[field] = "https://eltron.pl" + response.xpath("//a[contains(., 'Datasheet')]//@href").get()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Краткое описание"
            result[field] = response.css(".product-information-description p::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Характеристики"
            result[field] = my_tools.del_classes_from_html(response.css("table.product-parameters-table").get())
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            result[field] = " > ".join(
                [i.css("::text").get() for i in response.css(".navigation a span.description")[1:-1]])
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result
