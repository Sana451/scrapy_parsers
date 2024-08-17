import time
from decimal import Decimal
import re
import requests

import scrapy
from scrapy.shell import inspect_response
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
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

        # self.log("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # self.log(len(urls))
        # # self.log(urls)
        # self.log("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        for url in urls[:10]:
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"playwright": True}
            )
            # yield SeleniumRequest(url=url, callback=self.parse)

    def parse_product_page(self, response):
        # inspect_response(response, self)

        yield {
            "Заголовок товара": response.css("h1.product-details__name::text").get(),
            "Артикул (Order number)": response.css(
                "div.product-details__product-number::text"
            ).get(),
            # "Модель": "",
            "Цена": Decimal(
                response.css("p.price::text").get().strip().strip("€").replace(",", "")
            ),
            # "Цена со скидкой": "",
            "Наличие": response.css(
                "span.product-stock-level__localization::text"
            ).get(),
            "Картинки": f"https://norelem.de/{response.css('div.product-details-spacing img')[0].attrib['src']} | "
            f"https://norelem.de/{response.css('div.product-details-spacing img')[1].attrib['src']}",
            # "PDF": "",
            # "Краткое описание": "",
            # "Полное описание": "",
            # "Характеристики": "",
            # "Категории": "",
        }

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

            button.click()

            for i in range(50):
                ActionChains(driver).scroll_by_amount(0, i).perform()

            WebDriverWait(driver, 40).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div.product-table a[data-id]",
                    )
                )
            )
            a_tags = driver.find_elements(
                By.CSS_SELECTOR, "div.product-table a[data-id]"
            )

            # self.log("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # self.log(a_tags)
            # self.log("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            for a in a_tags:
                product_page = a.get_attribute("href")
                driver.close()
                yield scrapy.Request(product_page, callback=self.parse_product_page)
