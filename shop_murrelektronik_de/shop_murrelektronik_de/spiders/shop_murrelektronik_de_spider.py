import csv
import json
import sys

import requests
from parsel import Selector
from tabulate import tabulate

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

DOMAIN = "https://shop.murrelektronik.de"


class ShopMurrelektronikDeSpiderSpider(scrapy.Spider):
    name = "shop_murrelektronik_de_spider"
    allowed_domains = ["shop.murrelektronik.de"]

    def start_requests(self):
        with open(RESULTS_DIR / "shop.murrelektronik.de.links.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            start_urls = [row[0] for row in list(reader)[1:]]
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    headers=headers,
                    cookies=cookies,
                    dont_filter=True,
                )

    def parse(self, response):
        result = dict()

        result["url"] = response.url

        js = response.xpath("//*[@class='additionalInfo']//script[@type='application/ld+json']//text()").get().strip()
        data = json.loads(js)

        try:
            field = "Заголовок"
            title = data["name"]
            if title:
                result[field] = title.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул / SKU"
            sku = data["sku"]
            if sku:
                result[field] = sku.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "MPN"
            mpn = data["mpn"]
            if sku:
                result[field] = mpn.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "GTIN"
            gtin = data["gtin13"]
            if gtin:
                result[field] = gtin.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            price = data["offers"]["highPrice"]
            if price:
                result[field] = price
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена со скидкой"
            sale_price = get_sale_price(result["Артикул / SKU"])
            if sale_price:
                result[field] = sale_price
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Наличие"
            available = response.css(".additionalInfo .detailStockInfo::text").getall()
            if available:
                result[field] = "".join(available).strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Количество"
            count = response.css(".information .stockQuantity::text").get()
            if count:
                result[field] = count.strip().lstrip("(").rstrip(")")
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            images = response.xpath("//a[contains(@id, 'moreP')]//@href").getall()
            if images:
                result[field] = " | ".join(images)
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "PDF"
            pdf = response.xpath("//li[contains(., 'Product-PDF')]//a//@href").get()
            if not pdf:
                pdf = response.xpath("//li[contains(., 'Produkt-PDF')]//a//@href").get()
            if pdf:
                result[field] = DOMAIN + pdf
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Вес"
            weight = data["weight"]
            if weight:
                result[field] = weight.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Краткое описание"
            short_desc = response.css(".shortDescription::text").get()
            if short_desc:
                result[field] = short_desc.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Описание"
            desc = response.xpath("//*[@id='description']//text()").getall()
            if desc:
                result[field] = "".join([a.strip() for a in desc])
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Характеристики"
            details = response.css("#detailsAttributes #attributes table").getall()
            if short_desc:
                result[field] = "\n".join([my_tools.del_classes_from_html(t) for t in details])
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Коммерч. инф."
            commerce = response.css("div#detailsCommercialData div#attributes table").get()
            if commerce:
                result[field] = my_tools.del_classes_from_html(commerce)
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            cats = " > ".join(response.url.split("/")[4:-1])
            if cats:
                result[field] = cats
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

cookies = {
    "sid_key": "oxid",
    "visitor_id883653": "892544652",
    "visitor_id883653-hash": "5754bdd2b4eab77d9963edf2fc0056f55a4e6c146955a24c7a567f585f6e82b7dbb92532fabd963e33fce58d72357b1464c44794",
    "language": "0",
    "showlinksonce": "1",
    "oxid_1_autologin": "1",
    "oxid_1": "osl%40famaga.de%40%40%40%242y%2410%24dZo31hQK8PfmnWXz13nkhOUZbuSVgWnKYiF3duGW4S9PXFE2JhlJ.",
    "sid": "bnli4b73kafsaspgjhphbpecj6",
    "_uetsid": "60cdd09091c711ef8399f5ec510f824c",
    "_uetvid": "8351f910908311efa48421e1f63ace65"
}


def get_sale_price(article):
    cookies = {
        'sid_key': 'oxid',
        'visitor_id883653': '892544652',
        'visitor_id883653-hash': '5754bdd2b4eab77d9963edf2fc0056f55a4e6c146955a24c7a567f585f6e82b7dbb92532fabd963e33fce58d72357b1464c44794',
        'showlinksonce': '1',
        'oxid_1_autologin': '1',
        'oxid_1': 'osl%40famaga.de%40%40%40%242y%2410%24dZo31hQK8PfmnWXz13nkhOUZbuSVgWnKYiF3duGW4S9PXFE2JhlJ.',
        'sid': 'pars0ihmvi1467lbins9nl7ptq',
        'language': '1',
        '_uetsid': '60cdd09091c711ef8399f5ec510f824c',
        '_uetvid': '8351f910908311efa48421e1f63ace65',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'sid_key=oxid; visitor_id883653=892544652; visitor_id883653-hash=5754bdd2b4eab77d9963edf2fc0056f55a4e6c146955a24c7a567f585f6e82b7dbb92532fabd963e33fce58d72357b1464c44794; showlinksonce=1; oxid_1_autologin=1; oxid_1=osl%40famaga.de%40%40%40%242y%2410%24dZo31hQK8PfmnWXz13nkhOUZbuSVgWnKYiF3duGW4S9PXFE2JhlJ.; sid=pars0ihmvi1467lbins9nl7ptq; language=1; _uetsid=60cdd09091c711ef8399f5ec510f824c; _uetvid=8351f910908311efa48421e1f63ace65',
        'origin': 'https://shop.murrelektronik.de',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        # 'referer': 'https://shop.murrelektronik.de/en/M23-SERVO-CABLE-7000-PS411-8210300.html',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'artlist[0][artnum]': article,
        'artlist[0][amount]': '1',
        'cl': 'nfc_middleware_user_prices',
        'fnc': 'execute',
        'pageType': 'detail',
    }

    response = requests.post(
        'https://shop.murrelektronik.de/index.php',
        cookies=cookies,
        headers=headers,
        data=data)

    if "AN ERROR OCCURRED" in str(response.content):
        return ""
    else:
        data = json.loads(response.content)
        sale_price = data["updateListUserPrice"][article]["1"]["price"]
        return sale_price
