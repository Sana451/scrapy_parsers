import csv
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

cookies = {
    'session-2': 'uc07cqujmqdci77h2rskb340lu',
    'allowCookie': '1',
    'cookiePreferences': '{"groups":{"technical":{"name":"technical","cookies":{"allowCookie":{"name":"allowCookie","active":true},"cookieDeclined":{"name":"cookieDeclined","active":true},"csrf_token":{"name":"csrf_token","active":true},"cookiePreferences":{"name":"cookiePreferences","active":true},"currency":{"name":"currency","active":true},"slt":{"name":"slt","active":true},"nocache":{"name":"nocache","active":true},"x-cache-context-hash":{"name":"x-cache-context-hash","active":true},"paypal-cookies":{"name":"paypal-cookies","active":true},"shop":{"name":"shop","active":true},"session":{"name":"session","active":true}},"active":true},"comfort":{"name":"comfort","cookies":{"sUniqueID":{"name":"sUniqueID","active":true}},"active":false},"statistics":{"name":"statistics","cookies":{"partner":{"name":"partner","active":true},"wbm_tag_manager":{"name":"wbm_tag_manager","active":true},"x-ua-device":{"name":"x-ua-device","active":true}},"active":false}},"hash":"WyJhbGxvd0Nvb2tpZSIsImNvbWZvcnQiLCJjb29raWVEZWNsaW5lZCIsImNvb2tpZVByZWZlcmVuY2VzIiwiY3NyZl90b2tlbiIsImN1cnJlbmN5Iiwibm9jYWNoZSIsInBhcnRuZXIiLCJwYXlwYWwtY29va2llcyIsInNVbmlxdWVJRCIsInNlc3Npb24iLCJzaG9wIiwic2x0Iiwic3RhdGlzdGljcyIsInRlY2huaWNhbCIsIndibV90YWdfbWFuYWdlciIsIngtY2FjaGUtY29udGV4dC1oYXNoIiwieC11YS1kZXZpY2UiXQ=="}',
    'QEtRRWsNaGiCWKeD9M_Haris6Ho': 'KAjiSenxyAM9B90fok66Uv92y4s',
    'QEtRRWsNaGiCWKeD9M_Haris6Ho': 'KAjiSenxyAM9B90fok66Uv92y4s',
    'PiNItIMBs1PkgwNz_RpGEi9Icu4': '1728969470',
    'KUzx7IaDJL86Q4LxSIUAHx7gfuc': '1729055870',
    '--cv2u0HKbO9KRsgG1zDykal4mI': 'pfP85Hpgv4xDLPxYC7tofxfUkUY',
    '__csrf_token-2': 'Z8cMYbYhYnSkiBpUyAfafMUzwH2BOx',
    'session-1': 'ao4p6urahnm3a36p4i2tde777j',
    '__csrf_token-1': 'ubrFnga11Nr2oeEnJIIKceHCQ61ra3',
    'shop': '2',
    'currency': '1',
    'hubspotutk': '75d0249612114fbb19382a1e0ef233ce',
    '__hssrc': '1',
    'nocache': 'detail-2%2C%20detail-1',
    '__hstc': '9267242.75d0249612114fbb19382a1e0ef233ce.1728971805584.1728971805584.1728977693087.2',
    '__hssc': '9267242.1.1728977693087',
    'x-ua-device': 'tablet',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7',
    'cache-control': 'no-cache',
    # 'cookie': 'session-2=uc07cqujmqdci77h2rskb340lu; allowCookie=1; cookiePreferences={"groups":{"technical":{"name":"technical","cookies":{"allowCookie":{"name":"allowCookie","active":true},"cookieDeclined":{"name":"cookieDeclined","active":true},"csrf_token":{"name":"csrf_token","active":true},"cookiePreferences":{"name":"cookiePreferences","active":true},"currency":{"name":"currency","active":true},"slt":{"name":"slt","active":true},"nocache":{"name":"nocache","active":true},"x-cache-context-hash":{"name":"x-cache-context-hash","active":true},"paypal-cookies":{"name":"paypal-cookies","active":true},"shop":{"name":"shop","active":true},"session":{"name":"session","active":true}},"active":true},"comfort":{"name":"comfort","cookies":{"sUniqueID":{"name":"sUniqueID","active":true}},"active":false},"statistics":{"name":"statistics","cookies":{"partner":{"name":"partner","active":true},"wbm_tag_manager":{"name":"wbm_tag_manager","active":true},"x-ua-device":{"name":"x-ua-device","active":true}},"active":false}},"hash":"WyJhbGxvd0Nvb2tpZSIsImNvbWZvcnQiLCJjb29raWVEZWNsaW5lZCIsImNvb2tpZVByZWZlcmVuY2VzIiwiY3NyZl90b2tlbiIsImN1cnJlbmN5Iiwibm9jYWNoZSIsInBhcnRuZXIiLCJwYXlwYWwtY29va2llcyIsInNVbmlxdWVJRCIsInNlc3Npb24iLCJzaG9wIiwic2x0Iiwic3RhdGlzdGljcyIsInRlY2huaWNhbCIsIndibV90YWdfbWFuYWdlciIsIngtY2FjaGUtY29udGV4dC1oYXNoIiwieC11YS1kZXZpY2UiXQ=="}; QEtRRWsNaGiCWKeD9M_Haris6Ho=KAjiSenxyAM9B90fok66Uv92y4s; QEtRRWsNaGiCWKeD9M_Haris6Ho=KAjiSenxyAM9B90fok66Uv92y4s; PiNItIMBs1PkgwNz_RpGEi9Icu4=1728969470; KUzx7IaDJL86Q4LxSIUAHx7gfuc=1729055870; --cv2u0HKbO9KRsgG1zDykal4mI=pfP85Hpgv4xDLPxYC7tofxfUkUY; __csrf_token-2=Z8cMYbYhYnSkiBpUyAfafMUzwH2BOx; session-1=ao4p6urahnm3a36p4i2tde777j; __csrf_token-1=ubrFnga11Nr2oeEnJIIKceHCQ61ra3; shop=2; currency=1; hubspotutk=75d0249612114fbb19382a1e0ef233ce; __hssrc=1; nocache=detail-2%2C%20detail-1; __hstc=9267242.75d0249612114fbb19382a1e0ef233ce.1728971805584.1728971805584.1728977693087.2; __hssc=9267242.1.1728977693087; x-ua-device=tablet',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.twk.de/produkte/zubehoer/9264/vorflansch-fuer-drehgeber-modell-zhf',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}


class TwkDeSpiderSpider(scrapy.Spider):
    name = "twk_de_spider"
    allowed_domains = ["twk.de"]

    def start_requests(self):
        with open(RESULTS_DIR / "twk.de.links.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            start_urls = [row[0] for row in list(reader)[1:]]
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    cookies=cookies,
                    headers=headers
                    # meta={"playwright": True},
                )

    def parse(self, response):

        result = dict()

        result["url"] = response.url

        try:
            field = "Заголовок"
            title = response.css("h1.product--title::text").get()
            if title:
                result[field] = title.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            art = response.css("div.product--description::text").get()
            if art:
                result[field] = art.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Ключ заказа"
            order_key = response.css(".vdb-orderkey::text").get()
            if order_key:
                result[field] = order_key.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            price = response.css(".price--content::text").getall()
            if price:
                result[field] = price[-1].replace("€ *", "").replace(",", ".").strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Срок доставки"
            delivery = response.css(".delivery--text::text").getall()
            if delivery:
                result[field] = delivery[-1].strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            images = response.xpath("//*[contains(@class, 'image-slider--container')]//img//@srcset").get()
            if images:
                result[field] = " | ".join([url for url in images.split() if url.startswith("http")])
            else:
                result[field] = ""

        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "PDF"
            pdf = response.xpath("//div[contains(h3, 'Data sheet')]//*[contains(@class, 'en_GB')]/parent::a")
            if pdf:
                result[field] = " | ".join([a.attrib["href"] for a in pdf])
            else:
                result[field] = ""

        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Вес"
            weight = response.xpath("//td[contains(text(), 'Weight')]//following-sibling::td//text()").get()
            if weight:
                result[field] = weight.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Описание"
            result[field] = response.css(".product--description p::text").get()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Характеристики"
            details = response.css("table.product--properties-table").get()
            if details:
                result[field] = my_tools.del_classes_from_html(details)
            else:
                result[field] = ""

        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            result[field] = " > ".join(
                "https://www.twk.de/en/products/rotary-encoders/8843/rotary-encoder-trd?c=81".split("/")[5:-1])
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        return result
