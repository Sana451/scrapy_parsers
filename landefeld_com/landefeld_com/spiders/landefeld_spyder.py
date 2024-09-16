import csv
import re
import time
from pathlib import Path
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

import scrapy
from scrapy.shell import inspect_response
from selenium.webdriver.common.by import By
from tabulate import tabulate

# div.product - category - lister
# DOMAIN = "https://www.norgren.com"
CURRENT_DIR = Path("__file__").resolve()

BASE_DIR = CURRENT_DIR.parent
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors_only_links.csv"


def del_classes_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th", "target", "itemprop", "content"]:
            del tag[attribute]

    return str(soup)


def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(["class", "style", "id", "scope", "data-th", "target"]):
        data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


def create_html_table(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    res = []
    divs = soup.find_all("div")
    for div in divs:
        span_list = div.find_all("span")
        if len(span_list) == 2:
            res.append(i.text.strip() for i in span_list)
    # spans = soup.find_all("span")
    # for i in range(0, len(spans), 2):
    #     res.append((spans[i].text.strip(), spans[i + 1].text.strip()))

    html = tabulate(res, tablefmt="html").replace("\n", "")

    return html


def save_error(url, error, field, err_file_path=ERRORS_FILENAME):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


DOMAIN = "www.landefeld.com"


class LandefeldOnlyLinksSpider(scrapy.Spider):
    name = "only_links_spyder"
    allowed_domains = ["www.landefeld.com"]

    def start_requests(self):
        with open(RESULTS_DIR / "categories.csv") as cat_links_file:
            reader = csv.reader(cat_links_file)
            categories = list(reader)[:1]
            # articles = cat_links_file.readlines()[:1]

        # with open(RESULTS_DIR / "Product_export_20240912120700.csv") as cat_links_file:
        #     reader = csv.reader(cat_links_file)
        #     articles = list(reader)[1:2]

        # prefix = "https://www.landefeld.com/cgi/main.cgi?DISPLAY=suche&filter_suche_artikelmenge=&filter_suche_suchstring="
        for url in categories:
            url = url[0] + "?filterpath=1&page=42"
            # url = url[0] + "?filterpath=1&page=42"
            # url = f"{prefix}{art[2]}"

            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 # cb_kwargs={"art": art[2]},
                                 # meta={"playwright": True},
                                 )

    def parse(self, response):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        # options.page_load_strategy = 'eager'
        browser = webdriver.Chrome(options=options)
        # browser.get("https://www.landefeld.com/en")
        browser.get(response.url)
        # browser.get(browser.current_url.replace("/de/", "/en/"))

        try:
            shadow = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div#cmpwrapper")
                )
            )
            if shadow:
                shadow_root = shadow.shadow_root
                shadow_root.find_element(By.CSS_SELECTOR, "a.cmptxt_btn_yes").click()
        except TimeoutException as error:
            pass

        try:
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.pk-button")
                )
            ).click()
        except Exception:
            pass

        # shadow = browser.find_element(By.CSS_SELECTOR, "div#cmpwrapper")
        # shadow_root = shadow.shadow_root
        # shadow_root.find_element(By.CSS_SELECTOR, "a.cmptxt_btn_yes").click()
        #
        # browser.find_element(By.CSS_SELECTOR, "button.pk-button").click()

        all_links = []

        result = dict()

        time.sleep(1000)
        try:
            links = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.artikel-info-box-container a")
                )
            )
        except TimeoutException as error:
            save_error(browser.current_url, error, "Links not load")

        if links:
            links = browser.find_elements(By.CSS_SELECTOR, "div.artikel-info-box-container a")
            for i in range(0, len(links), 2):
                a = links[i].get_attribute("href")
                result["url"] = a

                result["Категория"] = response.url
                yield result
        else:
            result["url"] = "Не ссылок"

            result["Категория"] = response.url
            yield result

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback_only_links.csv")
