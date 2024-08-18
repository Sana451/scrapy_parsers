import time
from decimal import Decimal
import re
import requests

import scrapy
from scrapy.shell import inspect_response
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_cookie_bot(browser, url):
    browser.get(url)

    button = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
            )
        )
    )
    if isinstance(button, WebElement):
        button.click()
    else:
        click_cookie_bot(browser, url)


class FamilyLinksSpider(scrapy.Spider):
    name = "family_links"

    def start_requests(self):
        xml_url = "https://norelem.de/sitemap/en-de.xml"
        xml_page = requests.get(xml_url)
        soup = BeautifulSoup(xml_page.content, "xml")

        re_pattern = re.compile(r"^http.+/p/agid.\d+")
        urls = []
        for url in soup.find_all("loc"):
            if re_pattern.match(url.text):
                urls.append(url.text)

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "proxy": "http://168.228.47.129:9197:PHchyV:qvzX3m",
                },
            )

    def parse(self, response):
        browser = webdriver.Chrome()

        if response.css("button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"):
            click_cookie_bot(browser, response.url)

        table = False
        while table is False:
            for i in range(10):
                ActionChains(browser).scroll_by_amount(0, i).perform()
            try:
                table = WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "div.product-table a[data-id]",
                        )
                    )
                )
            except TimeoutException:
                pass

        a_tags = browser.find_elements(
            By.CSS_SELECTOR, "div.product-table a[data-id][href]"
        )
        links = [a.get_attribute("href") for a in a_tags]

        availabilityes = browser.find_elements(
            By.CSS_SELECTOR, "div.product-table .product-stock-level__lights[title]"
        )

        for link in links:
            yield {"product_links": link, "family_links": response.url}
            # inspect_response(response, self)

            # inspect_response(response, self)

            # for i in range(len(a_tags)):
            #     product_page = a_tags[i].get_attribute("href")
            #     self.availability = availabilityes[i].get_attribute("title")
            #     driver.close()

            # yield scrapy.Request(
            #     product_page,
            #     callback=self.parse_product_page,
            #     meta={
            #         "playwright": True,
            #         "proxy": "http://168.228.47.129:9197:PHchyV:qvzX3m",
            #     },
            # )


class ProductSpider(scrapy.Spider):
    name = "products"

    def start_requests(self):
        with open("./links.csv", "r") as file:
            read_file = file.readlines()
            for url in read_file[1:]:
                page_url = url.strip()

                self.log("\n\n!!!!!!!!!!!!!!!")
                self.log(page_url)
                self.log("\n\n!!!!!!!!!!!!!!!")

                yield scrapy.Request(
                    url=page_url,
                    callback=self.parse,
                    meta={
                        "playwright": True,
                        "proxy": "http://168.228.47.129:9197:PHchyV:qvzX3m",
                    },
                )

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

        yield {
            "Заголовок товара": response.css("h1.product-details__name::text").get(),
            # "Артикул (Order number)": response.css(
            #     "div.product-details__product-number::text"
            # ).get(),
            "Артикул (Order number)": response.css("span.active::text").get(),
            # "Модель": "",
            "Цена": Decimal(
                response.css("p.price::text").get().strip().strip("€").replace(",", "")
            ),
            "Цена со скидкой": "",
            # "Наличие": self.availability,
            # "Наличие": response.css(
            #     "span.product-stock-level__localization::text"
            # ).get(),
            # "Наличие": driver.find_element(
            #     By.CSS_SELECTOR, "span.product-stock-level__localization"
            # ).text,
            "Картинки": f"https://norelem.de/{response.css('div.product-details-spacing img')[0].attrib['src']} | "
            f"https://norelem.de/{response.css('div.product-details-spacing img')[1].attrib['src']}",
            # "PDF": "",
            # "Краткое описание": "",
            # "Полное описание": "",
            # "Характеристики": "",
            # "Категории": "",
        }
