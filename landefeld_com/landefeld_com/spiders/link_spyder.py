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
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


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


class LandefeldSpider(scrapy.Spider):
    name = "link_spyder"
    allowed_domains = ["www.landefeld.com"]

    def start_requests(self):
        with open(RESULTS_DIR / "Product_export_20240912120700.csv", encoding="utf-16") as cat_links_file:
            reader = csv.reader(cat_links_file, delimiter=";")
            articles = list(reader)[:20]
            # articles = cat_links_file.readlines()[:1]

        # with open(RESULTS_DIR / "Product_export_20240912120700.csv") as cat_links_file:
        #     reader = csv.reader(cat_links_file)
        #     articles = list(reader)[1:2]

        prefix = "https://www.landefeld.com/cgi/main.cgi?DISPLAY=suche&filter_suche_artikelmenge=&filter_suche_suchstring="
        for art in articles:
            url = f"{prefix}{art[2]}"

            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 cb_kwargs={"art": art[2]},
                                 # meta={"playwright": True},
                                 )

    def parse(self, response, art):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        browser = webdriver.Chrome(options=options)
        browser.get("https://www.landefeld.com/en")
        browser.get(response.url)
        browser.get(browser.current_url.replace("/de/", "/en/"))

        shadow = browser.find_element(By.CSS_SELECTOR, "div#cmpwrapper")
        shadow_root = shadow.shadow_root
        shadow_root.find_element(By.CSS_SELECTOR, "a.cmptxt_btn_yes").click()

        browser.find_element(By.CSS_SELECTOR, "button.pk-button").click()

        result = dict()
        result['Aртикль'] = art

        try:
            h1 = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h1[contains(text(), '')]")
                )
            )
        except Exception as error:
            result["Заголовок"] = "Не найден"
            save_error(browser.current_url, error, "Not h1")

        try:
            if "Search results for" in h1.text:
                result["Заголовок"] = "Не найден"
                result["url"] = ""
                result["Item number"] = ""
                result["Special item number"] = ""
                result["Цена"] = ""
                result["Наличие"] = ""
                result["Картинки"] = ""
                result["PDF"] = ""
                result["Характеристики"] = ""
            else:

                try:
                    field = "Заголовок"
                    result[field] = h1.text
                except Exception as error:
                    save_error(browser.current_url, error, field)

                try:
                    field = "url"
                    result[field] = browser.current_url.replace("/de/", "/en/")
                except Exception as error:
                    save_error(browser.current_url, error, field)

                try:
                    field = "Item number"
                    result[field] = browser.find_element(
                        By.CSS_SELECTOR, "div.artikelnr h2").text
                except Exception as error:
                    save_error(browser.current_url, error, field)

                try:
                    field = "Special item number"
                    result[field] = browser.find_element(
                        By.CSS_SELECTOR, "div.alternativeninfo span").text
                except Exception as error:
                    save_error(browser.current_url, error, field)

                try:
                    field = "Цена"
                    result[field] = browser.find_element(
                        By.CSS_SELECTOR, "div.aktuellerpreis").text.lstrip("€").rstrip(
                        "incl. VAT")
                except Exception as error:
                    save_error(browser.current_url, error, field)

                try:
                    field = "Наличие"
                    result[field] = browser.find_elements(
                        # By.CSS_SELECTOR, "div.lieferinfo span")[0].text
                        By.CSS_SELECTOR, "div.lieferinfo-abstand span").text
                except Exception as error:
                    save_error(browser.current_url, error, field)

                try:
                    field = "Картинки"
                    img = browser.find_element(
                        By.CSS_SELECTOR, "div.slide-bild-background").get_attribute('style')
                    result[field] = DOMAIN + re.match(r".+(/shop/media/.+\.jpg)", img).group(1)
                except Exception as error:
                    save_error(browser.current_url, error, field)

                try:
                    field = "PDF"
                    docs = browser.find_elements(
                        By.CSS_SELECTOR, "ul.dokumente a")
                    result[field] = " | ".join([a.get_attribute('href') for a in reversed(docs)])
                except Exception as error:
                    save_error(browser.current_url, error, field)

                try:
                    field = "Характеристики"
                    details = browser.find_element(
                        By.CSS_SELECTOR, "table.artikelauspraegung").get_attribute(
                        "outerHTML")
                    result["field"] = del_classes_from_html(details)
                except Exception as error:
                    save_error(browser.current_url, error, field)

            yield result

        except Exception as error:
            save_error(browser.current_url, error, "Not field")

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")
