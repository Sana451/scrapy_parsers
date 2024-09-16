import csv
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
DOMAIN = "https://www.norgren.com"
CURRENT_DIR = Path("__file__").resolve()

BASE_DIR = CURRENT_DIR.parent
RESULTS_DIR = BASE_DIR / "results"
LINKS_DIR = BASE_DIR / "links"
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
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        browser = webdriver.Chrome(options=options)
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

    def start_requests(self):
        with open(RESULTS_DIR / "cactegories_links.csv") as cat_links_file:
            reader = csv.reader(cat_links_file)
            start_urls = list(reader)[:1]

        for url in start_urls:
            yield scrapy.Request(url=url[0],
                                 callback=self.parse,
                                 # meta={"playwright": True},
                                 )

    def parse(self, response, **kwargs):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        browser = webdriver.Chrome(options=options)
        browser.get(response.url)
        # browser.implicitly_wait(5)
        urls = browser.find_elements(By.CSS_SELECTOR, "body h4 a")
        # inspect_response(response, self)
        # urls = response.css("div.product-category-lister a")
        # self.log("!!!!!!!!!!", len(urls))
        if urls:
            for url in urls:
                try:
                    yield {
                        "url": url.get_attribute('href')
                    }
                except Exception as error:
                    save_error(response.url, error, "links")
        # try:
        #     next_page = browser.find_element(By.CSS_SELECTOR, "link[rel='next']")
        # except NoSuchElementException:
        #     next_page = None
        #     browser.quit()
        # if next_page is not None:
        #     next_page_url = next_page.get_attribute("href")
        #     browser.quit()
        #     yield response.follow(next_page_url, callback=self.parse)

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")


TIMEOUT = 5


class NorgrenProductsSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ["www.norgren.com"]

    def start_requests(self):
        with open(RESULTS_DIR / "product_links_v5.csv") as cat_links_file:
            reader = csv.reader(cat_links_file)
            start_urls = list(reader)[1:]

        for url in start_urls:
            yield scrapy.Request(url=url[0],
                                 callback=self.parse,
                                 meta={"playwright": True},
                                 )

    def parse(self, response, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        browser = webdriver.Chrome(options=options)
        browser.get(response.url)
        # browser.implicitly_wait(5)
        try:
            WebDriverWait(browser, TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "ensAcceptAll"))
            ).click()
        except NoSuchElementException:
            pass
        try:
            WebDriverWait(browser, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Shipping')]"))
            )
        except TimeoutException as error:
            save_error(response.url, error, "Try WebDriverWait Shipping in parse")

        result = dict()
        result['url'] = browser.current_url

        try:
            field_name = "Заголовок"
            title = WebDriverWait(browser, TIMEOUT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.font__heavy"))
            )
            if title:
                result[field_name] = title.text
        except TimeoutException as error:
            save_error(browser.current_url, error, field_name)

        try:
            field_name = "Product number"
            # inspect_response(response, self)
            article = response.css("p.product-details__item--number::text").get()
            if article:
                result[field_name] = article.strip()
            else:
                result[field_name] = ""
        except Exception as error:
            save_error(response.url, error, field_name)

        # try:
        #     field_name = "Цена"
        #     price = WebDriverWait(browser, 20).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, "h4.product-details__basket--base-price"))
        #     )
        #     if price.get_attribute("innerHTML") == "Please login for price":
        #         result[field_name] = ""
        #     else:
        #         result[field_name] = price.get_attribute("innerHTML").strip("$")
        # except Exception as error:
        #     save_error(browser.current_url, error, field_name)

        try:
            field_name = "Дата доставки"
            div = WebDriverWait(browser, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-details__basket--shipping"))
            )
            shipping_date = div.find_element(By.XPATH, "//span[contains(text(), 'Shipping')]")
            if shipping_date:
                result[field_name] = shipping_date.text.strip("Norgren Shipping Date:")
            else:
                result[field_name] = ""

        except Exception as error:
            save_error(browser.current_url, error, field_name)

        try:
            field_name = "Наличие"
            div = WebDriverWait(browser, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-details__basket--stock"))
            )
            availability = div.find_element(By.TAG_NAME, "span")
            if availability:
                result[field_name] = availability.text
            else:
                result[field_name] = ""

        except Exception as error:
            save_error(browser.current_url, error, field_name)

        try:
            field_name = "Картинки"
            image = WebDriverWait(browser, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-details__listing img"))
            )
            if image:
                result[field_name] = image.get_attribute('src')
            else:
                result[field_name] = ""

        except Exception as error:
            save_error(browser.current_url, error, field_name)

        try:
            field_name = "PDF"
            pdf = response.css('#datasheet-download')
            if pdf:
                result[field_name] = pdf.attrib['href']
            else:
                result[field_name] = ""

        except Exception as error:
            save_error(browser.current_url, error, field_name)

        try:
            field_name = "Краткое описание"
            short_description = WebDriverWait(browser, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-details__spec--features"))
            )
            if short_description:
                short_description = short_description.get_attribute("outerHTML")
                result[field_name] = del_classes_from_html(short_description)

            else:
                result[field_name] = ""

        except Exception as error:
            save_error(browser.current_url, error, field_name)

        try:
            field_name = "Описание"
            description = WebDriverWait(browser, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-details__listing table"))
            )
            if description:
                description = description.get_attribute("outerHTML")
                result[field_name] = description
            else:
                result[field_name] = ""

        except Exception as error:
            save_error(browser.current_url, error, field_name)

        try:
            field_name = "Технические характеристики"
            technical_details = WebDriverWait(browser, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-details__product-data--table"))
            )
            if technical_details:
                technical_details = technical_details.get_attribute("innerHTML")
                result[field_name] = technical_details
            else:
                result[field_name] = ""

        except Exception as error:
            save_error(browser.current_url, error, field_name)

        browser.close()
        yield result

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")
