import csv
from decimal import Decimal

import scrapy
import bs4
from scrapy_playwright.page import PageMethod
from scrapy.shell import inspect_response
from selenium import webdriver
from tabulate import tabulate

from .spider_tools import (
    click_cookie_bot,
    HOSTNAME,
)

ERROR_FILE_NAME = "error_add_links2.csv"


def create_html_table(html: str) -> str:
    soup = bs4.BeautifulSoup(html, "html.parser")

    #     for tag in soup():
    #         for attribute in ["class"]:
    #             del tag[attribute]
    res = []
    for span in soup.find_all("span"):
        res.append((span.text, span.findNext().text))

    html = tabulate(res, tablefmt="html").replace("\n", "")

    return html


def get_price_or_inquiry_price(response):
    try:
        price = Decimal(
            response.css("p.price::text").get().strip().strip("€").replace(",", "")
        )
    except AttributeError:
        try:
            price = response.css(".price::text").get().strip().strip("€")
        except AttributeError:
            price = response.css("span.inquiry-price::text").get()
    return price


def get_pdf(response):
    try:
        pdf = f"{HOSTNAME}/{response.css('a.link-panel')[0].attrib['href']}"
    except IndexError:
        # pdf = response.css("div.tabbody div.download-tab__wrapper link-panel").attrib["link-url"]
        pdf = response.css("div.tabbody div.download-tab__wrapper link-panel")[0].attrib["link-url"]
    return pdf


class ProductSpider(scrapy.Spider):
    name = "products"

    custom_settings = {
        "CONCURRENT_REQUESTS": 8,
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 100000,  # milliseconds
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "timeout": 20 * 1000,  # 20 seconds
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "RETRY_TIMES": 5,
        "DUPEFILTER_DEBUG": True,
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 5,
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
        # "DUPEFILTER_CLASS": "scrapy.dupefilters.BaseDupeFilter",
    }

    def start_requests(self):
        error_product_urls = []

        with open("/home/sana451/PycharmProjects/scrapy_norelem/parsers/shop_norelem/shop_norelem/add_links2.csv",
                  "r") as csvfile:

            reader = csv.reader(csvfile)
            links_data = list(reader)

            # for row in links_data[1:]:  # Первый элемент - названия полей
            for row in links_data:  # Первый элемент - названия полей
                # page_url = row[0]
                page_url = "".join(row)
                # family_url = row[1]
                # self.log(
                #     f"page_url is {page_url}",
                # )
                # self.log(
                #     f"family_url {family_url}",
                # )
                try:

                    yield scrapy.Request(
                        # url="https://norelem.de/en/Product-overview/Clamping-technology/01000/Profiles/V-block-machined-all-sides-grey-cast-iron-or-aluminium/Prism-Support-grey-cast-iron/p/01640-02X100",
                        url=page_url,
                        callback=self.parse,
                        cb_kwargs={"error_product_urls": error_product_urls},
                        errback=self.errback,
                        # headers={('User-Agent', 'Mozilla/5.0')},
                        meta=dict(
                            playwright=True,
                            playwright_include_page=True,
                            # playwright_page_methods=[
                            #     PageMethod("wait_for_selector", "a#product-details-tab")
                            # ],
                            proxy="http://168.228.47.129:9197:PHchyV:qvzX3m",
                        ),
                    )
                except Exception as error:
                    error_product_urls.append(page_url)
                    with open(ERROR_FILE_NAME, "a") as error_csvfile:
                        writer = csv.writer(error_csvfile, delimiter=",")
                        writer.writerow([page_url, error, type(error)])
                        self.log(error_product_urls)
                    self.log(error)

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        with open(ERROR_FILE_NAME, "a") as error_csvfile:
            writer = csv.writer(error_csvfile, delimiter=",")
            writer.writerow([failure.request.url, failure, type(failure)])
            self.log(failure.request.cb_kwargs["error_product_urls"])
        await page.close()

    async def parse(self, response, error_product_urls):
        page = response.meta["playwright_page"]
        await page.close()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        browser = webdriver.Chrome(options=options)

        if response.css("button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"):
            click_cookie_bot(browser, response.url)

        browser.quit()
        # inspect_response(response, self)

        try:
            result_dict = {
                "Заголовок товара": response.css(
                    "h1.product-details__name::text"
                ).get(),
                "Order number": response.css(
                    "span.product-details__product-number-text::text"
                ).get(),
                "Цена": get_price_or_inquiry_price(response),
                "Наличие": response.css(
                    "span.product-stock-level__localization::text"
                ).get(),
                "Features": ", ".join(
                    [i.strip() for i in response.css("div.product-details__features::text").getall()]
                ),
                "PDF": get_pdf(response),
                "Картинки": " | ".join(
                    [
                        f"{HOSTNAME}{i.attrib['src']}"
                        for i in response.css("div.product-details-spacing img")
                        if "Thumbnail" not in i.attrib["src"]
                    ]
                ),
                "Характеристики (details)": create_html_table(
                    response.css("div.category-texts").get()
                ),
                "Категории": " > ".join(
                    [li.css("::text").get() for li in
                     response.css("div.breadcrumb-mobile__wrapper ol.breadcrumb li")[1:]]
                ),
                "url": response.url,
            }

            yield result_dict

        except Exception as error:
            # inspect_response(response, self)
            error_product_urls.append(response.url)
            with open(ERROR_FILE_NAME, "a") as error_csvfile:
                writer = csv.writer(error_csvfile, delimiter=",")
                writer.writerow([response.url, error, type(error)])
                self.log(error_product_urls)
            self.log(error)
