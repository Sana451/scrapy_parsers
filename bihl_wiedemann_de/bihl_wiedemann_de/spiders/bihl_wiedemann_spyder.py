import csv
import decimal
import re
import time
from pathlib import Path

import pyautogui
from bs4 import BeautifulSoup

import scrapy
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate

DOMAIN = "https://www.bihl-wiedemann.de"

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
    with open(err_file_path, "a", newline="", encoding="utf-8") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


PROXY_USERNAME = "vk0dUcb"
PROXY_PASSWORD = "Us5jxS8o88"


def enter_proxy_auth(proxy_username, proxy_password):
    time.sleep(10)
    pyautogui.typewrite(proxy_username)
    time.sleep(5)
    pyautogui.press('tab')
    time.sleep(5)
    pyautogui.typewrite(proxy_password)
    time.sleep(5)
    pyautogui.press('enter')


def open_a_page(driver, url):
    driver.get(url)


class BihlWiedemannSpyder(scrapy.Spider):
    name = "bihl_wiedemann_spyder"
    allowed_domains = ["www.bihl-wiedemann.de"]

    def start_requests(self):
        with open(RESULTS_DIR / "links_de.csv") as cat_links_file:
            reader = csv.reader(cat_links_file)
            start_urls = list(reader)

        # cookie_string = "cookie_consent=%7B%22consent%22:true,%22options%22:%5B%22vimeo%22,%22youtube%22,%22ganalytics%22,%22gads%22,%22bwt%22,%22wpga4%22,%22hotjar%22%5D,%22version%22:3%7D; _hjSessionUser_3884933=eyJpZCI6IjJkMGU2YjAyLWJhZmQtNTYwNi1iOGJjLTMzMGZlMDlkMzZjMyIsImNyZWF0ZWQiOjE3MjMxOTcyMTIxMTgsImV4aXN0aW5nIjp0cnVlfQ==; wp_ga4_customerGroup=NOT%20LOGGED%20IN; __utmz=193900990.1723202223.2.2.utmcsr=shop.bihl-wiedemann.de|utmccn=(referral)|utmcmd=referral|utmcct=/; fe_typo_user=8dd2ff652f506e6bb9baa9571b209fc2.c74f85f2256437b610fcba2cd4d47e572ee82613d8130b8b76a6c1b1e5dbd4cc; PHPSESSID=3qimvjr96b241oirsnrb2fo7ha; gwMagentoLoginState=; __utma=193900990.1765942858.1723197212.1723202223.1726496618.3; __utmc=193900990; __utmt=1; gw-ajax-requested=1; gwresourcelist=-; _gid=GA1.2.1777378800.1726496626; form_key=txr57b8ygLXb2kMi; gw-geo-country=eu%2C-%2C-%2C-%2C0%231726496639%23AdvOyLd7E3YY7nAlQMALIe6XAe9D7iA8B%2BGjrsSQk4%2Fns8lsoJ9Nr5Svlx7Mkl%2FCrJAcAVg7fuWTSXROebDujwsgZ1s5S79oYL%2BNVTP3BI6u8BpD%2F3RLhqFR365o%2FIgJwD0pcSnxEJfB7UypfgWB4CZQEdWASAKQxAh5ndY9IHe%2F6KvuogNKB%2FNXb3xtjtos6%2BgU3sY%2B4vACkbCbqTk1MQ80ZaRumKwJXArtZPsB9zS6MSw9sEkVVKq28WvHaxzKnQNquaYGVN908qpLOpKxMZVlCUCkdbAO2dhTROuTHVQmWm2aDAJqSGQgt7VlB3cJ4kpvW76jyOVSJnpZ8AVbaQ%3D%3D; gw-legal-space=eu; __utmb=193900990.2.10.1726496618; _ga_MQMNHHL8SY=GS1.1.1726496617.4.1.1726496639.38.0.0; _ga=GA1.2.81638953.1723197212; gwMagentoCartSummaryCount=0"
        # from http.cookies import SimpleCookie
        # cookie = SimpleCookie()
        # cookie.load(cookie_string)
        # my_cookies = {k: v.value for k, v in cookie.items()}

        for url in start_urls:
            yield scrapy.Request(url=url[0],
                                 callback=self.parse,
                                 errback=self.errback,
                                 # cookies=my_cookies,
                                 # meta={"playwright": True,
                                 #       "proxy": "socks5://178.62.79.49:16614"},
                                 )

    def parse(self, response, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        seleniumwire_options = {
            'proxy': {
                'http': 'http://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
                'https': 'https://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        browser = webdriver.Chrome(seleniumwire_options=seleniumwire_options,
                                   options=options)
        browser.get(response.url)

        try:
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.select-all"))
            ).click()
        except TimeoutError:
            pass

        try:
            WebDriverWait(browser, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#iFrameResizer0"))
            )

        except Exception:
            pass

        result = dict()
        result["url"] = response.url

        try:
            field = "Цена"
            price_usd = browser.find_element(
                By.CSS_SELECTOR, "span.price"
            ).text.replace("€", ""
                           ).replace(",", "")
            result[field] = price_usd
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        # try:
        #     field = "Цена (€)"
        #     result[field] = round(number=decimal.Decimal(float(price_usd) / 1.23), ndigits=2)
        # except Exception as error:
        #     result[field] = ""
        #     save_error(response.url, error, field)

        try:
            field = "Наличие"
            result[field] = browser.find_element(By.CSS_SELECTOR, "span.c-stock-info__label a").text
        except Exception as error:
            result[field] = ""
            save_error(response.url, error, field)

        browser.switch_to.default_content()  # переключиться с iframe на исходную страницу

        try:
            field = "Заголовок"
            title = response.css("h1.gwcatalog-product-detail__heading").css("span.product-title::text").get()
            if title:
                result[field] = title
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Артикул"
            order_id = response.css("h1.gwcatalog-product-detail__heading").css("span.product-order-id::text").get()
            if order_id:
                result[field] = order_id
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Картинки"
            main_image = response.css("#gw-product-detail-overview div.product-image a")
            if main_image:
                main_image = [DOMAIN + main_image.attrib["href"]]
            other_images = response.css("#gw-product-detail-overview div.product-additional-images li a")
            if other_images:
                other_images = [DOMAIN + a.attrib["href"] for a in other_images]
            all_images = main_image + other_images
            result[field] = " | ".join(all_images)

        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "PDF"
            datasheet = response.css("li.gwcatalog-product-detail__page-list__item .datasheet")
            if datasheet:
                result[field] = DOMAIN + datasheet.attrib["href"]
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Краткое описание"
            description = response.css("div.product-description p::text").get()
            if description:
                result[field] = description
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Краткие характеристики"
            highlights = response.css("div.highlights ul").get()
            if highlights:
                highlights = del_classes_from_html(highlights)
                result[field] = highlights
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Технические характеристики"
            details = response.css("div.product-attributes table").get()
            if details:
                details = del_classes_AND_divs_from_html(details)
                result[field] = details
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        try:
            field = "Категории"

            categories = response.url.split("/")[5:-1]
            if categories:
                result[field] = " > ".join(categories)
            else:
                result[field] = ""
        except Exception as error:
            save_error(response.url, error, field)

        browser.quit()
        yield result

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")

# from bihl_wiedemann_de.spiders.bihl_wiedemann_spyder import *
