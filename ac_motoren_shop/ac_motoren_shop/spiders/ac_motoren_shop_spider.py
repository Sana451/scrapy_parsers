import csv
import sys

if sys.platform == "linux":
    sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
elif sys.platform == "win32":
    sys.path.insert(0, r"D:\sana451\scrapy_parsers")
from tools import my_scraping_tools as my_tools

from pathlib import Path

import scrapy

BASE_DIR = Path("__file__").resolve().parent
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"

cookies = {
    "_GRECAPTCHA": "1",
    "timezone": "Europe/Moscow",
    "acris_cookie_landing_page": "/",
    "cookie-preference": "1",
    "session-": "ercacqd5m63fspq7tau07235id",
    "sw-states": "logged-in",
    "sw-cache-hash": "e3692e508bc4a3743344bb9eca601e27"
}


class AcMotorenShopSpiderSpider(scrapy.Spider):
    name = "ac_motoren_shop_spider"
    allowed_domains = ["ac-motoren.shop"]

    def start_requests(self):
        with open(RESULTS_DIR / "ac-motoren.shop.links.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            start_urls = [row[0] for row in list(reader)[1:]]
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url,
                    method='GET',
                    dont_filter=True,
                    cookies=cookies,
                    callback=self.parse
                )

    def parse(self, response):
        result = dict()
        result["url"] = response.url

        try:
            field = "Заголовок"
            title = response.css("h1.product-detail-name::text").get()
            if title:
                result[field] = title.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "SKU / Артикул"
            sku = response.css(".product-detail-ordernumber::text").get()
            if sku:
                result[field] = sku.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            price = response.css(".product-detail-price::text").get()
            if price:
                result[field] = price.replace("*", "").replace("€", "").strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Наличие"
            availability = response.css(".product-detail-buy .delivery-information::text").getall()
            if availability:
                result[field] = availability[-1].strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            images = response.css(".gallery-slider-thumbnails-item-inner img")
            if images:
                result[field] = " | ".join([
                    a.attrib['src'] for a in images[0:len(images) // 2]
                ])
            else:
                result[field] = response.css(".gallery-slider-single-image img").attrib['src']
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "PDF"
            pdf = response.xpath("//*[contains(text(), 'Data sheet')]//parent::div//a//@href").getall()
            if pdf:
                result[field] = " | ".join([a for a in pdf if 'DATENBLATT' in a])

            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        response.xpath("//*[contains(text(), 'Data sheet')]//parent::div//a//@href").getall()

        try:
            field = "Краткое описание"
            short_desc = response.css(".product-detail-buy .product-detail-description-text::text").get()
            if short_desc:
                result[field] = short_desc.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Описание"
            desc = response.css(".product-detail-description .product-detail-description-text::text").getall()
            if desc:
                result[field] = ".".join(desc).strip().replace(" .", ".")
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Характеристики"
            details = response.css(".product-detail-properties-table").get()
            if details:
                result[field] = my_tools.del_classes_from_html(details)
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            cats = response.css("ol.breadcrumb li span::text").getall()
            if details:
                result[field] = " > ".join(cats[1:])
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result
