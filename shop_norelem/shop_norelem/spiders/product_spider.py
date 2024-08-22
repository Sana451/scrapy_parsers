import csv
from decimal import Decimal

import scrapy
from selenium import webdriver


from .spider_tools import (
    click_cookie_bot,
    HOSTNAME,
)


class ProductSpider(scrapy.Spider):
    name = "products"

    def start_requests(self):
        with open("./links.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            links_data = list(reader)

            for row in links_data[1:]:  # Первый элемент - названия полей
                page_url = row[0]
                # family_url = row[1]

                yield scrapy.Request(
                    url=page_url,
                    callback=self.parse,
                    meta={
                        "playwright": True,
                        "proxy": "http://168.228.47.129:9197:PHchyV:qvzX3m",
                    },
                )

    def parse(self, response):
        # browser = webdriver.Chrome()
        #
        # if response.css("button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"):
        #     click_cookie_bot(browser, response.url)
        #
        # browser.quit()

        yield {
            "Заголовок товара": response.css("h1.product-details__name::text").get(),
            "Order number": response.css(
                "span.product-details__product-number-text::text"
            ).get(),
            "Цена": Decimal(
                response.css("p.price::text").get().strip().strip("€").replace(",", "")
            ),
            "Наличие": response.css(
                "span.product-stock-level__localization::text"
            ).get(),
            "Features": ", ".join(
                [
                    i.strip()
                    for i in response.css(
                        "div.product-details__features::text"
                    ).getall()
                ]
            ),
            "PDF": f"{HOSTNAME}/{response.css('a.link-panel').attrib['href']}",
            "Картинки": " | ".join(
                [
                    f"{HOSTNAME}{i.attrib['src']}"
                    for i in response.css("div.product-details-spacing img")
                    if "Thumbnail" not in i.attrib["src"]
                ]
            ),
            "Характеристики (details)": response.css("div.category-texts").get(),
            "Категории": " > ".join(
                [
                    li.css("::text").get()
                    for li in response.css(
                        "div.breadcrumb-mobile__wrapper ol.breadcrumb li"
                    )[1:]
                ]
            ),
            "url": response.url,
        }
