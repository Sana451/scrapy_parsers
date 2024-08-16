from pathlib import Path
import requests

import scrapy
from scrapy.shell import inspect_response
from bs4 import BeautifulSoup
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class QuotesSpider(scrapy.Spider):
    name = "norelem"

    # xml_page = scrapy.Request(xml_url)

    def start_requests(self):
        # urls = [
        #     "https://norelem.de/sitemap/en-de.xml",
        # ]
        xml_url = "https://norelem.de/sitemap/en-de.xml"
        xml_page = requests.get(xml_url)
        soup = BeautifulSoup(xml_page.content, "xml")
        urls = [url.find("loc").text.split()[0] for url in soup.find_all("url")]
        # for url in urls:
        #     link =
        #     links.append(link)
        self.log("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # self.log(urls)
        # self.log(type(urls))
        # self.log(links)
        # self.log(urls[0].find("loc").text)
        self.log("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        for url in urls:
            # yield scrapy.Request(url=link, callback=self.parse)
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        self.log(response.request.meta["driver"])

        # page = response.url.split("/")[-2]
        # if response.css("buttor#chooseVariant"):
        #     inspect_response(response, self)
        inspect_response(response, self)
