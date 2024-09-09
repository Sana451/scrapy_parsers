import csv
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import scrapy
from scrapy.shell import inspect_response
from selenium.webdriver.common.by import By

# div.product - category - lister
DOMAIN = "https://www.norgren.com"
CURRENT_DIR = Path("__file__").resolve()

BASE_DIR = CURRENT_DIR.parent.parent
RESULTS_DIR = BASE_DIR / "results"
LINKS_DIR = BASE_DIR / "links"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


def save_error(url, error, field, err_file_path=ERRORS_FILENAME):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


class NorgrenCategoryLinksSpider(scrapy.Spider):
    name = "norgren_category_links"
    allowed_domains = ["www.norgren.com"]

    # custom_settings = {
    #     "DOWNLOAD_HANDLERS": {
    #         "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    #         "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    #     },
    #     "TWISTED_REACTORTWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    # }

    def start_requests(self):
        start_urls = ["https://www.norgren.com/en/products/air-preparation",
                      "https://www.norgren.com/en/products/electric-motion",
                      "https://www.norgren.com/en/products/fittings-tubing-accessories",
                      "https://www.norgren.com/en/products/industrial-communication",
                      "https://www.norgren.com/en/products/actuators",
                      "https://www.norgren.com/en/products/pressure-sensors",
                      "https://www.norgren.com/en/products/vacuum",
                      "https://www.norgren.com/en/products/valves"
                      ]

        for url in start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 # meta={"playwright": True},
                                 )

    def parse(self, response, **kwargs):
        browser = webdriver.Chrome()
        browser.get(response.url)
        browser.implicitly_wait(5)

        urls = browser.find_elements(By.CSS_SELECTOR, "div.product-category-lister a")
        # inspect_response(response, self)
        # urls = response.css("div.product-category-lister a")
        # self.log("!!!!!!!!!!", len(urls))
        if urls:
            for url in urls:
                yield {
                    # "url": DOMAIN + url.attrib['href']
                    # "url": DOMAIN + url.get_attribute('href')
                    "url": url.get_attribute('href')
                }
        browser.close()

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")


class NorgrenLinksSpider(scrapy.Spider):
    name = "norgren_links"
    allowed_domains = ["www.norgren.com"]

    # custom_settings = {
    #     "DOWNLOAD_HANDLERS": {
    #         "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    #         "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    #     },
    #     "TWISTED_REACTORTWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    # }

    def start_requests(self):
        with open(RESULTS_DIR / "cactegories_links.csv") as cat_links_file:
            reader = csv.reader(cat_links_file)
            start_urls = list(reader)[1:]

        for url in start_urls:
            yield scrapy.Request(url=url[0],
                                 callback=self.parse,
                                 # meta={"playwright": True},
                                 )

    def parse(self, response, **kwargs):
        browser = webdriver.Chrome()
        browser.get(response.url)
        browser.implicitly_wait(5)

        urls = browser.find_elements(By.CSS_SELECTOR, "body h4 a")
        # inspect_response(response, self)
        # urls = response.css("div.product-category-lister a")
        # self.log("!!!!!!!!!!", len(urls))
        if urls:
            for url in urls:
                yield {
                    # "url": DOMAIN + url.attrib['href']
                    "url": DOMAIN + url.get_attribute('href')
                }
        next_page = browser.find_element(By.CSS_SELECTOR, "link[rel='next']")
        if next_page is not None:
            next_page_url = next_page.get_attribute("href")
            yield response.follow(next_page_url, callback=self.parse)

        browser.close()

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")
