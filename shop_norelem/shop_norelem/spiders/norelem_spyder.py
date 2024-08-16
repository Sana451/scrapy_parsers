import re
import requests

import scrapy
from scrapy.shell import inspect_response
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "norelem"

    def start_requests(self):
        xml_url = "https://norelem.de/sitemap/en-de.xml"
        xml_page = requests.get(xml_url)
        soup = BeautifulSoup(xml_page.content, "xml")

        re_pattern = re.compile(r"^http.+/p/agid.\d+")
        # re_pattern = re.compile(r"^http.+/p/[\d-]+")
        urls = []
        for url in soup.find_all("loc"):
            if re_pattern.match(url.text):
                urls.append(url.text)

        self.log("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.log(len(urls))
        self.log("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        for url in urls:
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"playwright": True}
            )
            # yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        # inspect_response(response, self)

        yield {
            # "Заголовок товара": "response.css('h1.product-details__name::text').get()",
            "Заголовок товара": "response.css('h1.product-details__name::text').get()",
            "Артикул": "",
            "Модель": "",
            "Цена": float(
                response.css(
                    "div.-is-family-page span.product-price__net-price span::text"
                )
                .get()
                .strip("€")
                .replace(",", ".")
            ),
            "Цена со скидкой": "",
            "Наличие": "",
            "Картинки": "",
            "PDF": "",
            "Краткое описание": "",
            "Полное описание": "",
            "Характеристики": "",
            "Категории": "",
        }
