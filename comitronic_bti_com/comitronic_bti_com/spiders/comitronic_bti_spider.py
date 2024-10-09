import csv
import json
import sys

import requests
from selenium import webdriver
from tabulate import tabulate

if sys.platform == "linux":
    sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
elif sys.platform == "win32":
    sys.path.insert(0, r"D:\sana451\scrapy_parsers")
from tools import my_scraping_tools as my_tools
from bs4 import BeautifulSoup

from pathlib import Path

import scrapy

BASE_DIR = Path("__file__").resolve().parent
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


class ComitronicBtiSpiderSpider(scrapy.Spider):
    name = "comitronic_bti_spider"
    allowed_domains = ["comitronic-bti.de"]
    browser = webdriver.Chrome()

    def start_requests(self):

        with open(RESULTS_DIR/"comitronic-bti.de.links.csv", "r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            start_urls = list(reader)
            for url in start_urls:
                yield scrapy.Request(
                    url=url[0],
                    callback=self.parse
                )

    def parse(self, response):
        result = {"url": response.url}

        yield result
