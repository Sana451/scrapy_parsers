import csv
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


HOSTNAME = "https://norelem.de"


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

        for url in urls[:2]:
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

        for link in links:
            yield {"product_links": link, "family_links": response.url}


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
