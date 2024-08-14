import requests

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Response


class PixsysSpider(scrapy.Spider):
    name = "pixsys"

    def start_requests(self):
        urls = [
            "https://shop.pixsys.net/en/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_product_links)

    def parse_product(self, response, **kwargs):
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
            "Краткое описание": response.css(
                "div#short_description_content span::text"
            ).get(),
            "Характеристики": response.css("table.table-data-sheet").get(),
            "Категории": " > ".join(
                response.css("span.navigation_page a span::text").getall()
            ),
        }

        try:
            description_link = response.css("div#short_description_content a").attrib[
                "href"
            ]
            if description_link:
                description_page = requests.get(description_link)
                if description_page.status_code == 200:
                    soup = BeautifulSoup(description_page.content, "html.parser")
                    description = soup.find("div", {"class": "product-description"})
                    data["Полное описание"] = description

                elif description_page.status_code == 404:
                    data["Полное описание"] = ""

        except KeyError:
            data["Полное описание"] = ""

        yield data

    def parse_product_links(self, response: Response):
        for page in response.css(
            "div#categories_block_left ul ul a::attr(href)"
        ).getall():
            yield scrapy.Request(url=page, callback=self.parse_product_links)
            product_links = response.css("a.product-name::attr(href)").getall()

            for product_link in product_links:
                yield scrapy.Request(product_link, callback=self.parse_product)
