from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import csv
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import scrapy

DOMAIN = "https://shop.ms-armaturen.com/"

CURRENT_DIR = Path("__file__").resolve()
BASE_DIR = CURRENT_DIR.parent
RESULTS_DIR = BASE_DIR / "results"
LINKS_DIR = BASE_DIR / "links"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


def save_error(url, error, field, err_file_path=ERRORS_FILENAME, *args, **kwargs):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


class ArmaturenLinkSpider(scrapy.Spider):
    name = "links_armaturen"

    custom_settings = {
        # "CONCURRENT_REQUESTS": 30,
        "RETRY_TIMES": 3,
        "DUPEFILTER_DEBUG": True,
        # "ROBOTSTXT_OBEY": False,
    }

    def start_requests(self):

        resposne = requests.get("https://shop.ms-armaturen.com")
        soup = BeautifulSoup(resposne.content)
        links = soup.select("div.cms-section li a")
        categories_hrefs = [DOMAIN + l['href'] + "?order=m-s-artikelnummer-aufsteigend&p=" for l in links]
        browser = webdriver.Chrome()
        browser.implicitly_wait(0.02)
        for start_url in categories_hrefs:
            i = 1
            next_page = True
            while next_page is True:
                url = start_url + str(i)
                browser.get(url)
                try:
                    not_found = browser.find_element(By.XPATH, "//div[contains(text(), 'No products found.')]")
                    if not_found is not None:
                        next_page = False
                except NoSuchElementException:
                    try:
                        page_404 = browser.find_element(By.XPATH, "//img[@alt='Page not found']")
                        next_page = False
                    except NoSuchElementException:

                        i += 1
                        yield scrapy.Request(url=url,
                                             callback=self.parse,
                                             errback=self.errback)

    def parse(self, response):

        soup = BeautifulSoup(response.text)
        links = soup.select("td a[class]")
        hrefs = [l['href'] for l in links]
        for href in hrefs:
            yield {
                "url": href
            }

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")

# from industriation_ru.spiders.link_spyder import *
