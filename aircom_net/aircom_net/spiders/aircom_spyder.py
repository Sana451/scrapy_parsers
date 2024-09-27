import csv
import json
import sys

import requests
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


class AircomSpyderSpider(scrapy.Spider):
    name = "aircom_spyder"
    allowed_domains = ["aircom.net"]

    def start_requests(self):
        with open(RESULTS_DIR / "links.aircom.csv", "r", encoding="utf-8") as links_file:
            reader = csv.reader(links_file)
            start_urls = list(reader)
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url[0],
                    callback=self.parse,
                    # meta={'proxy': 'http://vk0dUcb:Us5jxS8o88@23.27.3.254:59100'}
                )

    def parse(self, response):
        products = response.css("span.productName")
        pr_data = [pr.attrib["onclick"] for pr in products]
        for data in pr_data:
            pr_id_info = data.lstrip("productCheck(").rstrip(")").replace("'", "").split(",")
            prod_resp = make_post_sale_price(pr_id_info)
            soup = BeautifulSoup(prod_resp.content, "html.parser")
            # f = open("1.html", "w")
            # f.write(str(soup))
            # f.close()

            result = {"url": response.url}

            try:
                field = "Артикул"
                article = soup.select("#productName")[0]
                result[field] = article.text
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Заголовок"
                title = soup.find("h1")
                result[field] = title.text.strip()
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Версия"
                version = soup.select("p.productVersionName")[0]
                result[field] = version.text
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Цена"
                price = soup.select("span#oldPrice")[0]
                result[field] = price.text.replace("€", "")
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Цена со скидкой"
                price_sale = soup.select("span#realCurrentPrice")[0]
                result[field] = price_sale.text.replace("€", "")
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Группа"
                groups = soup.select("div.textHighlight")
                group = [g for g in groups if "Produktgruppe" in g.text][0]
                result[field] = group.text.strip("Produktgruppe:")
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Вес"
                groups = soup.select("div.textHighlight")
                weight = [g for g in groups if "Gewicht" in g.text][0]
                weight = weight.text.replace(r"\\n ", "").replace("Gewicht:", "").strip()
                result[field] = weight
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                fields = ["Наличие", "Дата поставки"]
                availability = soup.select("div#availabilityInfo")[0]
                if "green" in str(availability):
                    result[fields[0]] = availability.text.replace("\\n", "").strip()
                    result[fields[1]] = ""
                elif "red" in str(availability):
                    availability = soup.select("div#availabilityInfo span")[0]
                    result[fields[0]] = availability.text.strip()
                    shipment = soup.select("div#availabilityInfo")[0]

                    result[fields[1]] = shipment.text.replace(f"{result[fields[0]]}", ""
                                                              ).replace(
                        "Kürzere Lieferzeit anfragen!", "\nKürzere Lieferzeit anfragen!"
                    ).strip()

            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Картинки"
                image = soup.select("a#imageLink")[0]
                result[field] = image["href"]
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Описание"
                description = response.css("p#full-product-description").get().split("Anwendung")[0]
                mini_soup = BeautifulSoup(description, "html.parser")
                [tag.extract() for tag in mini_soup.select("br")]
                [tag.extract() for tag in mini_soup.select("b")]
                result[field] = mini_soup.text.strip()
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Характеристики"
                details = soup.select("#TechinfoContainer table")[0]
                cleaned_details = my_tools.del_classes_from_html(str(details))
                result[field] = cleaned_details
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Категории"
                categories = soup.select("div.product-breadcrumbs a")
                categories = [a["title"] for a in categories[1:]]
                result[field] = " > ".join(categories)
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            yield result


def make_post_sale_price(prod_info: list):
    resp = requests.post(
        url=f"https://www.aircom.net/de/Gruppe/{prod_info[3]},{prod_info[1]}/{prod_info[2]},{prod_info[0]}.htm",
        data='bForAjax=1&sHint=0',
        headers={
            "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
            "Accept-Language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.aircom.net",
            "Pragma": "no-cache",
            "Referer": "https://www.aircom.net/de/miniaturdruckregler/r364,175.html",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "X-Prototype-Version": "1.7",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\""
        },
        cookies={
            "CookieConsent": "{stamp:%27WhbVbjbr0V/Ja2MemL2Pb7eJh8BT+SCiGuoO/n7SY5mfej/9w2j3Dw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1727330583692%2Cregion:%27ru%27}",
            "PHPSESSID": "4irpulein7qjb15j8k5qjjhtni",
            "i_ProductGroupId": "30"
        },
        auth=(),
    )
    return resp
