import csv
import re
import sys
import time
from pathlib import Path

import scrapy_splash
from scrapy import Request
from scrapy_splash import SplashRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")

from tools import my_scraping_tools as my_tools
from bs4 import BeautifulSoup

import scrapy
from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC


# DOMAIN = "https://www.camlogic.it"

BASE_DIR = Path("__file__").resolve().parent

RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


# from http.cookies import SimpleCookie
#
# raw_cookies = """_gcl_au=1.1.1890166969.1726730539; all_ppc=true; ph_phc_iL74ayq5SuNJ2vq0tOu7ohb3Ybllchc1crKCtF9AWQ4_posthog=%7B%22distinct_id%22%3A%22cus_01HPK3C2QVVXSX9N46MZ7VGYSH%22%2C%22%24sesid%22%3A%5B1726732797188%2C%2201920929-13af-7211-94cc-fdd551ff4a36%22%2C1726730539951%5D%2C%22%24epp%22%3Atrue%7D; _dd_s=logs=1&id=a99c2ca0-82b3-49cc-86b8-6452bec61b3e&created=1726730545831&expire=1726734101167"""
# cookie = SimpleCookie()
# cookie.load(raw_cookies)
# cookies = {k: v.value for k, v in cookie.items()}


class FixpartLinkSpyder(scrapy.Spider):
    name = "fixpart_link_spyder"
    allowed_domains = ["flixpart.de"]

    def start_requests(self):
        with open("/home/sana451/PycharmProjects/scrapy_parsers/flixpart_de/flixpart_de/results/stauff.atricles.csv",
                  "r") as csv_file:
            reader = csv.reader(csv_file)
            articles = [column[1] for column in list(reader)]
            prefix = "https://www.flixpart.de/q?query="
            start_urls = [prefix + article for article in articles]

        for url in start_urls:
            yield scrapy.Request(url,
                                 # meta={"playwright": True, }
                                 )

    def parse(self, response):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        seleniumwire_options = {
            'proxy': {
                'http': 'http://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
                'https': 'https://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        browser = webdriver.Chrome(seleniumwire_options=seleniumwire_options, options=options)
        browser.get(response.url)

        try:
            # WebDriverWait(browser, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Akzeptieren')]"))
            # ).click()
            browser.find_element(By.XPATH, "//button[contains(text(), 'Akzeptieren')]").click()
        except Exception:
            pass

        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "p div.grid a",
                )
            )
        )
        result = dict()
        links = browser.find_elements(By.CSS_SELECTOR, "p div.grid a")
        hrefs = [a.get_attribute("href") for a in links]
        browser.quit()
        result["url"] = "\n".join(hrefs)
        yield result

    async def errback(self, failure):
        my_tools.save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")

# from bihl_wiedemann_de.spiders.bihl_wiedemann_spyder import *
