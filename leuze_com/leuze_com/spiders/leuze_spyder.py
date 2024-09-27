import csv
import sys
from pathlib import Path

import scrapy_splash
from scrapy_splash import SplashRequest


sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
from bs4 import BeautifulSoup

from tools import my_scraping_tools as my_tools

import scrapy

BASE_DIR = Path("__file__").resolve().parent

RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


class LeuzeSpyderSpider(scrapy.Spider):
    name = "leuze_spyder"
    allowed_domains = ["leuze.com"]

    def start_requests(self):
        with open(RESULTS_DIR / "links.csv", "r") as links_file:
            reader = csv.reader(links_file)
            start_urls = [url[0] for url in reader]

        for url in start_urls:
            # yield scrapy.Request(url,
            #                      meta={"playwright": True}
            #                      )
            yield SplashRequest(url, self.parse,
                                args={
                                    # optional; parameters passed to Splash HTTP API
                                    'wait': 0.5,

                                    # 'url' is prefilled from request url
                                    # 'http_method' is set to 'POST' for POST requests
                                    # 'body' is set to request body for POST requests
                                },
                                endpoint='render.json',  # optional; default is render.html
                                splash_url='<url>',  # optional; overrides SPLASH_URL
                                slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                )

    def parse(self, response):
        result = {"url": response.url}
        try:
            field = "Заголовок"
            result[field] = response.css("h1.product-detail-name::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_DIR / "field_errors.csv")

        try:
            field = "Артикул"
            result[field] = response.css(".product-detail-ordernumber::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_DIR / "field_errors.csv")

        try:
            field = "Модель/тип"
            result[field] = response.css("h2.product-detail-name::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_DIR / "field_errors.csv")

        field = "Цена"
        result[field] = ""

        # try:
        #     field = "Цена евро"
        #     price_pound = response.css("div.product-detail-price-container meta[itemprop=price]").attrib["content"]
        #     if price_pound:
        #         price = float(price_pound.replace(",", ""))
        #         price_euro = round(1.096 * float(price), 2)
        #     result[field] = price_euro
        # except Exception as error:
        #     try:
        #         result[field] = response.css("div.product-detail-content div.alert-content::text").get().strip()
        #     except Exception:
        #         result[field] = ""
        #         my_scraping_tools.save_error(response.url, error, field, ERRORS_DIR / "field_errors.csv")

        try:
            field = "Наличие"
            availability = response.css(".product-detail-main .delivery-available"
                                        ).xpath("//*[contains(text(), 'Available immediately')]"
                                                ).css("::text").get()
            if availability:
                availability = availability.strip()
            elif availability := response.css(".product-detail-main .delivery-available"
                                              ).xpath("//*[contains(text(), 'Delivery to be confirmed')]"
                                                      ).css("::text").get():
                availability = availability.strip()
            else:
                availability = response.css(".product-detail-main .delivery-available::text")[1].get().strip()
            result[field] = availability
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_DIR / "field_errors.csv")

        try:
            field = "Картинки"
            images = response.css(".gallery-slider-item img")
            if images:
                images = set(images)
                images = " | ".join([img.attrib['src'] for img in images])
            result[field] = images
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_DIR / "field_errors.csv")

        try:
            field = "PDF"
            pdf = response.xpath(
                "//div[contains(text(), 'Data sheet - pdf')]/following::i[@class='flag-icon flag-icon-us'][1]/parent::a"
            )
            if pdf:
                pdf = pdf.attrib['href']
            result[field] = pdf
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_DIR / "field_errors.csv")

        try:
            field = "Характеристики"
            details = response.css("div.product-detail-tabs-content table")
            details = [my_tools.del_classes_from_html(table.get()) for table in details]
            result[field] = "\n".join(details)
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_DIR / "field_errors.csv")

        try:
            field = "Категории"
            categories = response.css("nav[aria-label=breadcrumb] li span")
            if categories:
                cats = " > ".join([span.css("::text").get() for span in categories[1:]])
            result[field] = cats
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_DIR / "field_errors.csv")

        yield response.follow(response.url.replace("/en-uk/", "/de-de/"), callback=self.found_price, cb_kwargs={
            "result": result
        })

    def found_price(self, response, result):
        try:
            field = "Цена"
            price_pound = response.css("div.product-detail-price-container meta[itemprop=price]").attrib["content"]
            result[field] = float(price_pound.replace(",", ""))
        except Exception as error:
            try:
                result[field] = response.css("div.product-detail-content div.alert-content::text").get().strip()
            except Exception:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_DIR / "field_errors.csv")
        yield result
