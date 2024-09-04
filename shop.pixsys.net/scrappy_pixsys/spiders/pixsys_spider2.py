import csv
import re

import requests

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Response
from scrapy.shell import inspect_response
from tabulate import tabulate

ERROR_FILE_NAME = "/home/sana451/PycharmProjects/scrapy_norelem/parsers/shop.pixsys.net/pixsys_errors.csv"


def save_error(url, error, path):
    with open(path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile, delimiter=",")
        writer.writerow([url, type(error), error])


def del_classes_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup():
        for attribute in ["class", "style"]:
            del tag[attribute]
    # res = []
    # for span in soup.find_all("span"):
    #     res.append((span.text, span.findNext().text))
    #
    # html = tabulate(res, tablefmt="html").replace("\n", "")
    #
    # return html
    return soup


def get_specifications(response):
    spec = response.css("table.table-data-sheet").get()
    if spec:
        return del_classes_from_html(spec)
    else:
        return ""


def get_short_description(response):
    try:
        short_description = response.css(
            "div#short_description_content span::text"
        ).get()
        if short_description is None:
            short_description = response.css(
                "div#short_description_content div::text"
            ).get()
    except Exception as error:
        save_error(response.url, error, ERROR_FILE_NAME)

    return short_description


class PixsysSpider(scrapy.Spider):
    name = "pixsys"

    def start_requests(self):
        xml_url = "https://shop.pixsys.net/1_en_0_sitemap.xml"
        xml_page = requests.get(xml_url)
        soup = BeautifulSoup(xml_page.content, "xml")

        re_pattern = re.compile(r"http.+.html")
        urls = []
        for url in soup.find_all("loc"):
            if re_pattern.match(url.text):
                urls.append(url.text)

        error_product_urls = []

        for url in urls:
            try:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_product,
                    cb_kwargs={"error_product_urls": error_product_urls},
                    errback=self.errback,
                )
            except Exception as error:
                save_error(url, error, ERROR_FILE_NAME)

    def errback(self, failure):
        with open(ERROR_FILE_NAME, "a") as error_csvfile:
            writer = csv.writer(error_csvfile, delimiter=",")
            writer.writerow([failure.request.url, type(failure), failure])

    def parse_product(self, response, error_product_urls):

        try:
            data = {
                "URL страницы": response.url,
                "Заголовок": response.css("h1::text").get(),
                "Модель/Тип": response.css("span.navigation_page::text").get(),
                "Condition": response.css("p#product_condition span::text").get(),
                "Reference": response.css("span.editable:nth-child(2)::text").get(),
                "Цена": float(
                    response.css("div.box-info-product #our_price_display").attrib[
                        "content"
                    ]
                ),
                "Наличие": response.css("#availability_value::text").get(),
                "Картинки": response.css("img#bigpic").attrib["src"],
                "Краткое описание": get_short_description(response),
                "Характеристики": get_specifications(response),
                "Категории": " > ".join(
                    response.css("span.navigation_page a span::text").getall()
                ),
            }

            try:
                description_link = response.css(
                    "div#short_description_content a"
                ).attrib["href"]
                if description_link:
                    description_page = requests.get(description_link)
                    if description_page.status_code == 200:
                        soup = BeautifulSoup(description_page.content, "html.parser")
                        description = soup.find("div", {"class": "product-description"})
                        data["Полное описание"] = del_classes_from_html(str(description))

                    elif description_page.status_code == 404:
                        data["Полное описание"] = ""

            except KeyError:
                data["Полное описание"] = ""

            yield data

        except Exception as error:
            # inspect_response(response, self)
            save_error(response.url, error, ERROR_FILE_NAME)

    # def parse_product_links(self, response: Response):
    #     for page in response.css(
    #         "div#categories_block_left ul ul a::attr(href)"
    #     ).getall():
    #         yield scrapy.Request(url=page, callback=self.parse_product_links)
    #         product_links = response.css("a.product-name::attr(href)").getall()
    #
    #         for product_link in product_links:
    #             yield scrapy.Request(product_link, callback=self.parse_product)
