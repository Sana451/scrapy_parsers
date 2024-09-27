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
from seleniumwire import webdriver
from tabulate import tabulate

# DOMAIN = "https://www.flixpart.de"

BASE_DIR = Path("__file__").resolve().parent.parent

RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"

FIELDNAMES = ['url', 'Заголовок', 'Производитель', 'Название товара производителя',
              'Артикул производителя', 'Код типа производителя', 'Описание', 'Цена',
              'Цена со скидкой', 'Скидка', 'Доставка в теч.раб.дней', 'Доставка',
              'Срок доставки', 'Вес', 'Картинки', 'Доп.информация', 'Характеристики',
              'Категории']


def del_classes_AND_divs_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    [d.decompose() for d in soup.find_all("div")]

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name", "aria-label", "role"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def del_classes_from_html(html) -> str:
    if not isinstance(html, BeautifulSoup):
        soup = BeautifulSoup(html, "html.parser")
    else:
        soup = html
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


def scrapy_page(browser, url):
    fieldnames = []
    try:
        browser.get(url)

        result = dict()

        field = "url"
        fieldnames.append(field)
        try:
            result[field] = browser.current_url
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Заголовок"
            fieldnames.append(field)
            result[field] = browser.find_element(By.CSS_SELECTOR, "#product-info h1").text
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Производитель"
            fieldnames.append(field)
            result[field] = browser.find_element(By.CSS_SELECTOR, "#product-info h2").text
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Название товара производителя"
            fieldnames.append(field)
            result[field] = browser.find_element(
                By.XPATH, "//span[contains(text(), 'Hersteller-Artikelname')]/following-sibling::span").text
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Артикул производителя"
            fieldnames.append(field)
            result[field] = browser.find_element(
                By.XPATH, "//span[contains(text(), 'Hersteller-Artikelnummer')]/following-sibling::span").text
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Код типа производителя"
            fieldnames.append(field)
            result[field] = browser.find_element(
                By.XPATH, "//span[contains(text(), 'Hersteller-Typenschlüssel')]/following-sibling::span").text
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Описание"
            fieldnames.append(field)
            result[field] = browser.find_element(
                By.XPATH, "//span[contains(text(), 'Hersteller-Artikelbeschreibung')]/following-sibling::span").text
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Цена"
            fieldnames.append(field)
            # WebDriverWait(browser, 5).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, "//span[contains(text(), 'Originalpreis')]/following-sibling::span")
            #     )
            # )
            result[field] = browser.find_element(
                By.XPATH, "//span[contains(text(), 'Originalpreis')]/following-sibling::span"
            ).text.replace("€", "")
        except Exception:
            try:
                result[field] = browser.find_element(By.CSS_SELECTOR, "span.text-xl-semi").text.replace("€", "")
            except Exception as error:
                result[field] = ""
                save_error(url, error, field)

        try:
            field = "Цена со скидкой"
            fieldnames.append(field)
            # WebDriverWait(browser, 5).until(
            #     EC.presence_of_element_located(
            #         (By.CSS_SELECTOR, "span.text-indigo-600")
            #     )
            # )
            result[field] = browser.find_element(By.CSS_SELECTOR, "span.text-indigo-600"
                                                 ).text.replace("€", "")
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Скидка"
            fieldnames.append(field)
            # WebDriverWait(browser, 5).until(
            #     EC.presence_of_element_located(
            #         (By.CSS_SELECTOR, "span.text-indigo-500")
            #     )
            # )
            result[field] = browser.find_element(By.CSS_SELECTOR, "span.text-indigo-500"
                                                 ).text.replace("-", "")
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Доставка в теч.раб.дней"
            fieldnames.append(field)
            # WebDriverWait(browser, 5).until(
            #     EC.presence_of_element_located(
            #         (By.CSS_SELECTOR, "div.pt-2")
            #     )
            # )
            result[field] = browser.find_element(By.XPATH, "//span[contains(text(), 'Lieferung in')]"
                                                 ).text.replace("Lieferung in", "").replace("Werktagen*", "")
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Доставка"
            fieldnames.append(field)
            result[field] = browser.find_element(
                By.XPATH, "//span[contains(text(), 'Lieferung in')]/following-sibling::div/span[1]"
            ).text
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Срок доставки"
            fieldnames.append(field)
            result[field] = browser.find_element(
                By.XPATH, "//span[contains(text(), 'Lieferung in')]/following-sibling::div/span[2]"
            ).text.split(",")[1]
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Вес"
            fieldnames.append(field)
            result[field] = browser.find_element(
                By.XPATH, "//td[contains(text(), 'Einzelgewicht')]/following-sibling::td"
            ).text
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Картинки"
            fieldnames.append(field)
            image = browser.find_element(By.CSS_SELECTOR, "span.absolute img.object-contain").get_attribute("src")
            result[field] = image
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Характеристики"
            fieldnames.append(field)
            details = browser.find_elements(
                By.CSS_SELECTOR, "table.min-w-full")
            details = del_classes_from_html(details[0].get_attribute("outerHTML"))
            result[field] = details
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Доп.информация"
            fieldnames.append(field)
            details = browser.find_elements(
                By.CSS_SELECTOR, "table.min-w-full")
            soup = BeautifulSoup(details[1].get_attribute("outerHTML"), "html.parser")
            soup.find("span", attrs={"role": "img"}).decompose()
            details = del_classes_from_html(soup)
            result[field] = details
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        try:
            field = "Категории"
            fieldnames.append(field)
            categoryes = browser.find_elements(By.CSS_SELECTOR, "nav li a")
            cats = [cat.text for cat in categoryes[1:]]
            result[field] = " > ".join(cats)
        except Exception as error:
            result[field] = ""
            save_error(url, error, field)

        return result

    except Exception as error:
        print("browser get error")
        save_error(url, error, "browser get", RESULTS_DIR / "errback.csv")
        epmty_result = {name: "" for name in FIELDNAMES}
        epmty_result["url"] = url
        return epmty_result


# PROXY = "vk0dUcb:Us5jxS8o88@23.27.3.254:59100"


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    seleniumwire_options = {
        'proxy': {
            'http': 'http://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
            'https': 'https://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    browser = webdriver.Chrome(seleniumwire_options=seleniumwire_options, options=options)
    browser.implicitly_wait(7)
    browser.get("https://www.flixpart.de/account/login")

    try:
        # WebDriverWait(browser, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Akzeptieren')]"))
        # ).click()
        browser.find_element(By.XPATH, "//button[contains(text(), 'Akzeptieren')]").click()
    except Exception as error:
        save_error(browser.current_url, error, "Cookie bot")

    try:
        # form = WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "form.w-full"))
        # )
        form = browser.find_element(By.CSS_SELECTOR, "form.w-full")
        form.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys("osl@famaga.de")
        form.find_element(By.CSS_SELECTOR, "input[type=password]").send_keys("Famaga2024")
        form.find_element(By.CSS_SELECTOR, "button.w-full").click()
    except Exception as error:
        save_error(browser.current_url, error, "Login error")

    with open(RESULTS_DIR / "flixpart.de_links.csv") as cat_links_file:
        reader = csv.reader(cat_links_file)
        start_urls = list(reader)[5936:]

    with open(RESULTS_DIR / "res.csv", "a") as sel_res_file:
        writer = csv.DictWriter(sel_res_file,
                                fieldnames=FIELDNAMES)
        # writer.writeheader()

        for url in start_urls:
            new = url[0].split("://")
            new.insert(1, "://www.")
            url = "".join(new)
            print(url)
            res = scrapy_page(browser, url)
            writer.writerow(res)
