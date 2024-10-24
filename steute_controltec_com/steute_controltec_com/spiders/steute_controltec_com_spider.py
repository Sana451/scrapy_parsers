import csv
import re
import sys

from pathlib import Path

import requests
import scrapy
from bs4 import BeautifulSoup
from tabulate import tabulate

if sys.platform == "linux":
    sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
elif sys.platform == "win32":
    sys.path.insert(0, r"D:\sana451\scrapy_parsers")
from tools import my_scraping_tools as my_tools

BASE_DIR = Path("__file__").resolve().parent
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"

DOMAIN = "https://www.steute-controltec.com"


class SteuteControltecComSpiderSpider(scrapy.Spider):
    name = "steute_controltec_com_spider"
    allowed_domains = ["steute-controltec.com"]

    def start_requests(self):
        with open(RESULTS_DIR / "steute-controltec.com.links.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            start_urls = [row[0] for row in list(reader)[1:]]
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                )

    def parse(self, response):
        result = dict()

        result["url"] = response.url

        try:
            field = "Заголовок"
            title = response.css("h1.product__headline::text").get()
            if title:
                result[field] = title.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            art = response.xpath("//*[contains(text(),'Artikel-Nr.:') and not(contains(text(),'Alte'))]//text()").get()
            if art:
                result[field] = art.replace("Artikel-Nr.:", "").strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Alter артикул"
            alt = response.xpath("//*[@class='product__materialnumber']//*[contains(text(),'Alte')]//text()").get()
            if alt:
                result[field] = alt.replace("Alte\xa0Artikel-Nr.:", "").strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        data_num = response.xpath("//button[@data-comparison-button]//@data-comparison-button").get()
        c_hash = response.xpath("//*[@class='product__price']//@data-weco-pricerequest").get()
        if c_hash:
            c_hash = re.search(re.compile(r"cHash=(.+)"), c_hash).groups()[0]

        if data_num and c_hash:
            price_and_amount_soup = BeautifulSoup(get_price_request(data_num, c_hash), "html.parser")

        try:
            field = "Цена"
            price = price_and_amount_soup.select(".product__price__number")
            if price:
                result[field] = price[0].text.strip().replace(" €", "")
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Наличие"
            amount = price_and_amount_soup.select(".product__amount p")
            if amount:
                result[field] = amount[0].text.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            images = response.xpath("//*[@class='product__gallery']//a//@href").getall()
            if images:
                result[field] = " | ".join([DOMAIN + image for image in images])
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "PDF"
            pdf = response.xpath("//*[@id='downloadForm']//a[@class='stretched-link']//@href").getall()
            # pdf = response.xpath("//*[contains(@href, 'datasheets/de')]//@href").get()
            if pdf:
                result[field] = " | ".join([DOMAIN + href for href in pdf])
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Вес"
            weight = response.xpath("//*[contains(text(), 'Gewicht')]//following-sibling::p//text()").get()
            if weight:
                result[field] = weight.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Краткое описание"
            short_desc = response.css(".product__features__item ul").get()
            if short_desc:
                result[field] = my_tools.del_classes_from_html(short_desc)
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Характеристики"
            details = response.css(".product__technicaldata__content__inner")
            if details:
                titles = [d for d in details.css("h4")]
                titles = ["".join(t.css("::text").getall()) for t in titles]
                texts = [d for d in details.css("p::text").getall()]
                table = [(titles[i], texts[i]) for i in range(len(titles))]
                html_table = tabulate(table, tablefmt="html")
                clean_table = my_tools.del_classes_from_html(html_table)
                result[field] = clean_table
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            cats = response.css(".breadcrumb li a")
            if cats:
                result[field] = " > ".join([c.css("::text").get() for c in cats][1:])
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result


def get_price_request(data_num, c_chash):
    params = {
        'tx_ofweco_pricerequest[action]': 'priceRequest',
        'tx_ofweco_pricerequest[article]': data_num,
        'tx_ofweco_pricerequest[controller]': 'Weco',
        'cHash': c_chash,
    }

    response = requests.get(
        'https://www.steute-controltec.com/de/produkt/weco/pricerequest',
        params=params,
    )
    return response.json()["view"]
