import csv
import re
import time
from pathlib import Path

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import scrapy
from scrapy.shell import inspect_response
from selenium import webdriver
from tabulate import tabulate

DOMAIN = "https://www.camlogic.it"

BASE_DIR = Path("__file__").resolve().parent

RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


def del_classes_AND_divs_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    [d.decompose() for d in soup.find_all("div")]

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def del_classes_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name", "href", "title"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(["class", "style", "id", "scope", "data-th", "target"]):
        data.decompose()

    return ' '.join(soup.stripped_strings)


def create_html_table(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    res = []
    divs = soup.find_all("div")
    for div in divs:
        span_list = div.find_all("span")
        if len(span_list) == 2:
            res.append(i.text.strip() for i in span_list)

    html = tabulate(res, tablefmt="html").replace("\n", "")

    return html


def save_error(url, error, field, err_file_path=ERRORS_FILENAME):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


class CamlogicItSpyder(scrapy.Spider):
    # custom_settings = {
    #     "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    #     "DOWNLOAD_HANDLERS": {
    #         "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    #         "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    #     },
    #     "DUPEFILTER_DEBUG": True,
    #     "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    # }
    name = "camlogic_it_spyder"
    allowed_domains = ["www.camlogic.it"]
    start_urls = []

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    # PROXY = "vk0dUcb:Us5jxS8o88@23.27.3.254:59100"
    # options.add_argument(f"--proxy-server={PROXY}")
    browser = webdriver.Chrome(options=options)
    # browser.implicitly_wait(20)
    browser.get("https://www.camlogic.it/en/login?redir=%2Fen%2Fuser")

    def start_requests(self):
        with open(RESULTS_DIR / "links.csv") as cat_links_file:
            reader = csv.reader(cat_links_file)
            start_urls = list(reader)[:2]

        for url in start_urls:
            yield scrapy.Request(url=url[0],
                                 callback=self.parse,
                                 errback=self.errback,
                                 # meta={
                                     #     # "playwright": True,
                                     # "proxy": "http://168.228.47.129:9197:PHchyV:qvzX3m",
                                     # "proxy": "168.228.47.129:9197",
                                 # },
                                 )

    def parse(self, response):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        # PROXY = "vk0dUcb:Us5jxS8o88@23.27.3.254:59100"
        # options.add_argument(f"--proxy-server={PROXY}")
        browser = webdriver.Chrome(options=options)
        # browser.implicitly_wait(20)
        browser.get("https://www.camlogic.it/en/login?redir=%2Fen%2Fuser")

        try:
            WebDriverWait(browser, 5).until(
                EC.presence_of_all_elements_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            accept_cookie_btn = browser.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
            accept_cookie_btn.click()
        except Exception:
            pass

        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.ID, "customerSignInForm"))
            )
            form = browser.find_element(By.ID, "customerSignInForm")
            form.find_element(By.CSS_SELECTOR, "input[type=email]").send_keys("osl@famaga.de")
            form.find_element(By.CSS_SELECTOR, "input[type=password]").send_keys("FamagaKitov777!")
            form.find_element(By.ID, "front-remember-me-cb").click()
            browser.find_element(By.CSS_SELECTOR, "button.loginSubmitBtn").click()
        except Exception:
            pass

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-header"))
        )

        time.sleep(2)
        browser.get(response.url)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.prod-code"))
        )

        result = dict()
        result["url"] = response.url

        try:
            field = "Заголовок"
            result[field] = browser.find_element(By.CSS_SELECTOR, "h1.prod-code").text
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "Commercial code"
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".sellCode"))
            )
            result[field] = browser.find_element(By.CSS_SELECTOR, ".sellCode").text
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "Configuration code"
            result[field] = browser.find_element(By.CSS_SELECTOR, ".configurationCode").text
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "Цена"
            result[field] = browser.find_element(By.CSS_SELECTOR, "div.card-body span.full_price"
                                                 ).text.replace("€", "")
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "Цена со скидкой"
            result[field] = browser.find_element(By.CSS_SELECTOR, "div.card-body span.discounted_price"
                                                 ).text.replace("€", "")
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "Скидка"
            result[field] = browser.find_element(By.CSS_SELECTOR, "#productDetailConfigurator span.discount_label"
                                                 ).text.replace("Discount", "")
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "Картинки"
            images = browser.find_elements(By.CSS_SELECTOR, "img.img-web-ext")
            images_src = [img.get_attribute("src") for img in images if "placeholder" not in img.get_attribute("src")]
            result[field] = " | ".join(images_src)
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "PDF"
            div = browser.find_element(By.CSS_SELECTOR, "div#collapse_tech")
            pdf = div.find_element(By.XPATH, "//a[contains(text(), 'Technical datasheet')]")
            result[field] = pdf.get_attribute("href")
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "Описание"
            description = browser.find_element(By.CSS_SELECTOR, "div.prod-desc p").text
            result[field] = description
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "Technical Specifications"
            details = browser.find_element(
                By.CSS_SELECTOR, "div.productDetailAdvantages div.info-wrapper ul").get_attribute("outerHTML")

            result[field] = details
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "Specifications"
            specs = browser.find_elements(By.CSS_SELECTOR, "div.prod-desc ul")
            all_specs = [spec.get_attribute("outerHTML") for spec in specs]
            result[field] = "\n".join(all_specs)
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        try:
            field = "Категории"
            product_line = browser.find_element(By.XPATH, "//p[contains(text(), 'Product line')]")
            category = product_line.find_element(By.TAG_NAME, "a").text
            result[field] = category
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        browser.quit()
        yield result

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")

# from bihl_wiedemann_de.spiders.bihl_wiedemann_spyder import *
