import requests
from bs4 import BeautifulSoup

DOMAIN = "https://shop.ms-armaturen.com/"

import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import scrapy
from scrapy.shell import inspect_response
from tabulate import tabulate

# SITEMAP_URL = "https://industriation.ru/sitemap/"

CURRENT_DIR = Path("__file__").resolve()
BASE_DIR = CURRENT_DIR.parent
RESULTS_DIR = BASE_DIR / "results"
LINKS_DIR = BASE_DIR / "links"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


def save_error(url, error, field, err_file_path=ERRORS_FILENAME, *args, **kwargs):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


class ArmaturenLinkSpider(scrapy.Spider):
    name = "links_armaturen"

    custom_settings = {
        # "CONCURRENT_REQUESTS": 30,
        "RETRY_TIMES": 3,
        "DUPEFILTER_DEBUG": True,
        # "ROBOTSTXT_OBEY": False,
    }

    def start_requests(self):

        resposne = requests.get("https://shop.ms-armaturen.com")
        soup = BeautifulSoup(resposne.content)
        links = soup.select("div.cms-section li a")
        categories_hrefs = [DOMAIN + l['href'] for l in links]

        for url in categories_hrefs:
            yield scrapy.Request(url=url[0],
                                 callback=self.parse,
                                 errback=self.errback)




        # for group_link in only_AirTac_products:
        #     group_link_soup = BeautifulSoup(requests.get(group_link).content)
        #     airtag_links = [a["href"] for a in group_link_soup.select("div.product-card div.name a")]
        #     urls.extend(airtag_links)
        #     with open(LINKS_DIR / "links.csv", "a") as link_file:
        #         writer = csv.writer(link_file)
        #         for link in airtag_links:
        #             writer.writerow([link])



    def parse(self, response):

        soup = BeautifulSoup(response.text)
        links = soup.select("td a")
        hrefs = [l['href'] for l in links]
        for href in hrefs:
            yield {
                "url": href
            }

        # result = dict()

        # try:
        #     field_name = "url"
        #     result[field_name] = response.url
        # except Exception as error:
        #     save_error(response.url, error, field_name)
        #
        # try:
        #     field_name = "Артикул"
        #     # inspect_response(response, self)
        #     article = response.css(".product-detail-ordernumber::text").get()
        #     if article:
        #         result[field_name] = article.strip()
        #     else:
        #         result[field_name] = ""
        # except Exception as error:
        #     save_error(response.url, error, field_name)

        # yield result

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")

# from industriation_ru.spiders.link_spyder import *
