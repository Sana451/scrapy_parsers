import csv
from decimal import Decimal

import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import ElementNotInteractableException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ERROR_FILE_NAME = "/home/sana451/PycharmProjects/scrapy_norelem/parsers/elmeko/elmeko/elmeko_errors.csv"

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--headless=new")


def click_cookie(browser):
    button = WebDriverWait(browser, 1).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//a[@aria-label='allow cookies']",
            )
        )
    )
    if isinstance(button, WebElement):
        button.click()


def save_error(url, error, err_file_path=ERROR_FILE_NAME, field=""):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, type(error), error, field])


def del_classes_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th"]:
            del tag[attribute]

    return str(soup)
    # res = []
    # for span in soup.find_all("span"):
    #     res.append((span.text, span.findNext().text))
    #
    # html = tabulate(res, tablefmt="html").replace("\n", "")
    #
    # return html


class ProductsSpider(scrapy.Spider):
    name = "elmeko_prod"

    custom_settings = {
        "CONCURRENT_REQUESTS": 8,
        "RETRY_TIMES": 3,
        "DUPEFILTER_DEBUG": True,
        "ROBOTSTXT_OBEY": False,
        # "DOWNLOAD_DELAY": 20,
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }

    def start_requests(self):

        with open("/home/sana451/PycharmProjects/scrapy_norelem/parsers/elmeko/elmeko/elmeko_link_results.csv",
                  "r") as csvfile:
            reader = csv.reader(csvfile)
            urls = list(reader)[1:]
        # urls = [
        #     "https://www.elmeko.de/en/products/schaltschrank-klimatisierung/kuhlen/peltier-kuhlgerat-pk-30-2-ag/",
        #     "https://www.elmeko.de/en/details/filterlufter-lv-300",
        # ]
        for url in urls:
            yield scrapy.Request(url=url[0],
                                 # yield scrapy.Request(
                                 #     url="https://www.elmeko.de/en/products/schaltschrank-zubehor/massebander/flachbanderder-massebander-vpe-10-stuck",
                                 callback=self.parse_product,
                                 errback=self.errback, )

    def errback(self, failure):
        save_error(failure.request.url, failure)

    def parse_product(self, response):

        browser = webdriver.Chrome(options=options)
        browser.get(response.url)
        if browser.find_elements(By.XPATH, "//a[@aria-label='allow cookies']"):
            click_cookie(browser)

        result = dict()

        result["url"] = response.url

        try:
            result["Заголовок"] = response.css(".page-title span::text").get()
        except Exception as error:
            save_error(response.url, error, field="Заголовок")

        try:
            article = response.xpath("//div[@itemprop='sku']/text()").get()
            result["Артикул"] = article
        except Exception as error:
            save_error(response.url, error, field="Артикул")

        try:
            product_name = response.xpath("//td[@data-th = 'Product Name']/text()").get()
            result["Product Name"] = product_name.strip()
        except Exception as error:
            save_error(response.url, error, field="Product Name")

        try:
            price = response.css(".product-info-main span.price::text").get()
            # result["Цена"] = Decimal(price.strip("€"))
            result["Цена"] = price.strip("€")
        except Exception as error:
            save_error(response.url, error, field="Цена")

        try:
            delivery_time = response.xpath("//td[@data-th = 'Delivery time']/text()").get()
            result["Срок доставки"] = delivery_time.strip()
        except Exception as error:
            save_error(response.url, error, field="Срок доставки")

        try:
            color_span = browser.find_elements(By.XPATH, "//span[contains(text(),'Color')]")
            if color_span:
                fset = browser.find_elements(By.CSS_SELECTOR, "#product-options-wrapper .fieldset select")
                for field in fset:
                    select = Select(field)
                    select.select_by_index(1)
                colors = [var.text for var in select.options[1:]]
                result["Цвет"] = " | ".join(colors)
            else:
                result["Цвет"] = ""
        except Exception as error:
            save_error(response.url, error, field="Цвет")

        try:
            img_divs = browser.find_elements(By.XPATH, "//div[contains(@class, 'fotorama__img')]")
            img_links = [i.get_attribute('href') for i in img_divs if i.get_attribute('href')]
            result["Картинки 2"] = " | ".join(img_links)
        except Exception as error:
            save_error(response.url, error, field="Картинки")

        try:
            img = response.xpath("//img[@alt='main product photo']").attrib['src']
            # img_divs = browser.find_elements(By.XPATH, "//div[contains(@class, 'fotorama__img')]")
            # img_links = [i.get_attribute('href') for i in img_divs if i.get_attribute('href')]
            # result["Картинки"] = " | ".join(img_links)
            result["Картинки"] = img
        except Exception as error:
            save_error(response.url, error, field="Картинки")

        # try:
        #     # img_divs = browser.find_elements(By.XPATH, "//div[contains(@class, 'fotorama__stage__frame')]")
        #     img_divs = browser.find_elements(By.CSS_SELECTOR, ".fotorama__img")
        #     img_links = [i.get_attribute('href') for i in img_divs if i.get_attribute('href')]
        #     result["Картинки"] = " | ".join(img_links)
        #     result["Картинки"] = img_divs[0].get_attribute('href'), img_divs[1].get_attribute('href')
        # except Exception as error:
        #     save_error(response.url, error, field="Картинки")

        try:
            try:
                downloads_link = WebDriverWait(browser, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#tab-label-downloads-title"))
                )
                browser.refresh()
                downloads_link = WebDriverWait(browser, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#tab-label-downloads-title"))
                )
            except TimeoutException as error:
                save_error(response.url, error, field="PDF")
            # browser.find_element(By.CSS_SELECTOR, "#tab-label-downloads-title")
            if downloads_link:
                try:
                    downloads_link.click()
                except ElementNotInteractableException:
                    pass
            try:
                links = browser.find_elements(By.CSS_SELECTOR, "a.download_pdf")
                result["PDF"] = " | ".join([link.get_attribute('href') for link in links])
            except Exception as error:
                result["PDF"] = ""
                save_error(response.url, error, field="PDF")

        except Exception as error:
            save_error(response.url, error, field="PDF")

        try:
            description = response.css("div.description ul").get()
            if not description:
                description = response.css(".description").get()
            if description:
                result["Краткое описание"] = del_classes_from_html(description)
            else:
                result["Краткое описание"] = ""
        except Exception as error:
            save_error(response.url, error, field="Краткое описание")

        try:
            additional = response.css("div#additional table").get()
            if additional:
                result["Доп.информация"] = del_classes_from_html(additional)
            else:
                result["Доп.информация"] = ""
        except Exception as error:
            save_error(response.url, error, field="Доп.информация")

        try:
            weight = response.xpath("//th[contains(text(), 'Weight')]/..").css("td::text").get()
            if weight:
                result["Вес"] = weight.strip()
            else:
                result["Вес"] = ""
        except Exception as error:
            save_error(response.url, error, field="Вес")

        try:
            categories_link = browser.find_element(By.CSS_SELECTOR, ".back-categories a")
            categories_link.click()
            all_li = browser.find_elements(By.CSS_SELECTOR, "ul.items li")
            categories = [li.text for li in all_li[2:]]
            if categories:
                result["Категории"] = " > ".join(categories)
            else:
                result["Категории"] = ""
        except Exception as error:
            save_error(response.url, error)

        browser.close()

        yield result
