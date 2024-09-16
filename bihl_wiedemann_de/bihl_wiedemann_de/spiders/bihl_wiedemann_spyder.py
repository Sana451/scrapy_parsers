import csv
import re
from pathlib import Path

from bs4 import BeautifulSoup

import scrapy
from tabulate import tabulate

DOMAIN = "https://www.bihl-wiedemann.de"

BASE_DIR = Path("__file__").resolve().parent

RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


def del_classes_AND_divs_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    [d.decompose() for d in soup.find_all("div")]

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def del_classes_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name", "href", "title"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(["class", "style", "id", "scope", "data-th", "target"]):
        data.decompose()

    return ' '.join(soup.stripped_strings)


def create_html_table(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    res = []
    divs = soup.find_all("div")
    for div in divs:
        span_list = div.find_all("span")
        if len(span_list) == 2:
            res.append(i.text.strip() for i in span_list)

    html = tabulate(res, tablefmt="html").replace("\n", "")

    return html


def save_error(url, error, field, err_file_path=ERRORS_FILENAME):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


class BihlWiedemannSpyder(scrapy.Spider):
    name = "bihl_wiedemann_spyder"
    allowed_domains = ["www.bihl-wiedemann.de"]

    def start_requests(self):
        with open(RESULTS_DIR / "links.csv") as cat_links_file:
            reader = csv.reader(cat_links_file)
            start_urls = list(reader)[:5]

        for url in start_urls:
            yield scrapy.Request(url=url[0],
                                 callback=self.parse,
                                 errback=self.errback
                                 )

    def parse(self, response, **kwargs):
        result = dict()
        result["url"] = response.url

        try:
            field = "Заголовок"
            title = response.css("h1.gwcatalog-product-detail__heading").css("span.product-title::text").get()
            if title:
                result[field] = title
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Артикул"
            order_id = response.css("h1.gwcatalog-product-detail__heading").css("span.product-order-id::text").get()
            if order_id:
                result[field] = order_id
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Картинки"
            main_image = response.css("#gw-product-detail-overview div.product-image a")
            if main_image:
                main_image = [DOMAIN + main_image.attrib["href"]]
            other_images = response.css("#gw-product-detail-overview div.product-additional-images li a")
            if other_images:
                other_images = [DOMAIN + a.attrib["href"] for a in other_images]
            all_images = main_image + other_images
            result[field] = " | ".join(all_images)

        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "PDF"
            datasheet = response.css("li.gwcatalog-product-detail__page-list__item .datasheet")
            if datasheet:
                result[field] = DOMAIN + datasheet.attrib["href"]
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Краткое описание"
            description = response.css("div.product-description p::text").get()
            if description:
                result[field] = description
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Краткие характеристики"
            highlights = response.css("div.highlights ul").get()
            if highlights:
                highlights = del_classes_from_html(highlights)
                result[field] = highlights
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Технические характеристики"
            details = response.css("div.product-attributes table").get()
            if details:
                details = del_classes_AND_divs_from_html(details)
                result[field] = details
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Категории"

            categories = response.url.split("/")[5:-1]
            if categories:
                result[field] = " > ".join(categories)
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        yield result

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")

# from bihl_wiedemann_de.spiders.bihl_wiedemann_spyder import *
