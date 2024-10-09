import csv
import json
import re
import sys
import time

import requests
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from tabulate import tabulate

if sys.platform == "linux":
    sys.path.insert(0, "/")
elif sys.platform == "win32":
    sys.path.insert(0, r"D:\sana451\scrapy_parsers")
# from tools import my_scraping_tools as my_tools
from bs4 import BeautifulSoup

from pathlib import Path

BASE_DIR = Path("__file__").resolve().parent
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


def del_classes_from_html(html) -> str:
    if not isinstance(html, BeautifulSoup):
        soup = BeautifulSoup(html, "html.parser")
    else:
        soup = html
    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name", "href", "title", "cellpadding", "cellspacing", "width",
                          "data-cell", "data-table", "draggable", "data-tbody"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def save_error(url, error, field, err_file_path):
    with open(err_file_path, "a") as error_csvfile:
        csv_writer = csv.writer(error_csvfile)
        csv_writer.writerow([url, field, type(error), error])


FIELDNAMES = [
    'url',
    'Заголовок',
    'Артикул',
    'Цена от',
    'Цена без скидки',
    'Скидка',
    'Цена со скидкой',
    # 'Обозначение',
    'Картинки',
    'Описание',
    'Характеристики',
    'Категории',
]


def parse(url, browser):
    global FIELDNAMES
    browser.get(url)
    iter_res = []

    modifications = browser.find_elements(By.CSS_SELECTOR, "table.table tbody tr.text-center")
    if not modifications:
        modifications = [1, ]

    for mod in modifications:
        result = {}
        field = "url"
        result[field] = browser.current_url

        try:
            field = "Заголовок"
            title = browser.find_element(By.TAG_NAME, "h1")
            result[field] = title.text.strip()
        except Exception as error:
            result[field] = ""
            save_error(browser.current_url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            article = mod.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
            result[field] = article.get_attribute("innerHTML").strip()
        except Exception as error:
            result[field] = ""
            save_error(browser.current_url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена от"
            price = browser.find_element(By.CSS_SELECTOR, ".text-4xl")
            result[field] = price.text.replace("€", "").strip()
        except Exception as error:
            result[field] = ""
            save_error(browser.current_url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена без скидки"
            full_price = mod.find_element(By.CSS_SELECTOR, "td:nth-child(3) span s")
            if not full_price:
                raise Exception
            result[field] = full_price.get_attribute("innerHTML").replace("€", "").replace("&nbsp;", "").strip()
        except Exception:
            try:
                full_price = browser.find_element(By.XPATH, "//*[@data-panier-target='prix']//span[@class]/s")
                result[field] = full_price.get_attribute("innerHTML").replace("€", "").replace("&nbsp;", "").strip()
            except Exception as error:
                result[field] = ""
                save_error(browser.current_url, error, field, ERRORS_FILENAME)

        try:
            field = "Скидка"
            discount = mod.find_element(By.CSS_SELECTOR, "td:nth-child(3) span span[class]")
            if not discount:
                raise Exception
            result[field] = discount.get_attribute("innerHTML").replace("(-", "").replace(")", "").strip()
        except Exception:
            try:
                discount = browser.find_element(By.XPATH, "//*[@data-panier-target='prix']//span[contains(@class,'text-2xl')]")
                result[field] = discount.get_attribute("innerHTML").split("(")[-1].replace("-", "").replace(")", "").strip()
            except Exception as error:
                result[field] = ""
                save_error(browser.current_url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена со скидкой"
            sale_price = mod.find_element(By.CSS_SELECTOR, "td:nth-child(3) span:nth-child(3)")
            if not sale_price:
                raise Exception
            result[field] = sale_price.get_attribute("innerHTML").replace("€", "").replace("&nbsp;", "").strip()
        except Exception:
            try:
                sale_price = browser.find_element(By.XPATH, "//*[@class='text-4xl text-danger']")
                result[field] = sale_price.get_attribute("innerHTML").replace("€", "").replace("&nbsp;", "").strip()
            except Exception as error:
                result[field] = ""
                save_error(browser.current_url, error, field, ERRORS_FILENAME)

        # try:
        #     field = "Обозначение"
        #     desc = mod.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
        #     result[field] = desc.get_attribute("innerHTML").strip()
        # except Exception as error:
        #     result[field] = ""
        #     save_error(browser.current_url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            images = browser.find_elements(By.CSS_SELECTOR, ".carousel-inner img")
            images = [img.get_attribute("src") for img in images]
            result[field] = " | ".join(images)
        except Exception as error:
            result[field] = ""
            save_error(browser.current_url, error, field, ERRORS_FILENAME)

        try:
            field = "Описание"
            description = browser.find_element(By.CSS_SELECTOR, "#tabContentProduit p.lead")
            result[field] = description.get_attribute("innerHTML").strip()
        except Exception as error:
            result[field] = ""
            save_error(browser.current_url, error, field, ERRORS_FILENAME)

        try:
            field = "Характеристики"
            specifications = browser.find_element(By.XPATH, "//table[@data-table]")
            specifications = specifications.get_attribute("outerHTML")
            result[field] = del_classes_from_html(specifications)
        except Exception:
            try:
                specifications = browser.find_element(By.CSS_SELECTOR, ".ge-content ul")
                specifications = specifications.get_attribute("outerHTML")
                result[field] = del_classes_from_html(specifications)
            except Exception as error:
                result[field] = ""
                save_error(browser.current_url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            categories = browser.find_elements(By.CSS_SELECTOR, "ol.breadcrumb li a span")
            cats = [cat.text for cat in categories[1:-1]]
            result[field] = " > ".join(cats)
        except Exception as error:
            result[field] = ""
            save_error(browser.current_url, error, field, ERRORS_FILENAME)

        iter_res.append(result)

    return iter_res


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=options)
    browser.get("https://www.comitronic-bti.de/de/connexion-client")
    login = browser.find_element(By.ID, "login_username")
    login.send_keys("famaga")
    login.send_keys(Keys.ENTER)
    password = browser.find_element(By.ID, "login_password")
    password.send_keys("123456")
    password.send_keys(Keys.ENTER)
    btn = browser.find_element(By.XPATH, "//button[@class='btn btn-primary text-center']")
    btn.send_keys(Keys.ENTER)
    time.sleep(7)

    with open(RESULTS_DIR / "comitronic-bti.de.links.csv", "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        start_urls = list(reader)

        with open(RESULTS_DIR / "comitronic-bti.de.csv", "w", encoding="utf-8") as res_csv:
            writer = csv.DictWriter(res_csv, fieldnames=FIELDNAMES)
            writer.writeheader()
            for url in start_urls[:]:
                res = parse(url[0], browser)
                for iter_res in res:
                    writer.writerow(iter_res)

        browser.quit()
        browser = None
