import time
from decimal import Decimal
import re
import requests

import scrapy
from scrapy.shell import inspect_response
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        # self.log(urls)
        self.log("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        for url in urls[:5]:
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"playwright": True}
            )
            # yield SeleniumRequest(url=url, callback=self.parse)

    # def parse_family_links(self, response):
    #     # product_links = response.css("div.product-table a[data-id]").getat
    #     inspect_response(response, self)

    def parse(self, response):
        # inspect_response(response, self)

        if response.css("button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"):
            driver = webdriver.Chrome()
            driver.get(response.url)
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
                    )
                )
            )
            # button = driver.find_element(
            #     By.CSS_SELECTOR,
            #     "button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
            # )
            button.click()
            driver.close()
        inspect_response(response, self)

        yield {
            # "Заголовок товара": "response.css('h1.product-details__name::text').get()",
            "Заголовок товара": response.css(
                "h1.product-family-details__heading::text"
            ).get(),
            "Артикул": "",
            "Модель": "",
            "Цена": Decimal(
                response.css(
                    "div.-is-family-page span.product-price__net-price span::text"
                )
                .get()
                .strip("€")
                .replace(",", "")
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
