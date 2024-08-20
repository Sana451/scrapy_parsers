import time
import re
import requests

import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .spider_tools import click_cookie_bot


class FamilyLinksSpider(scrapy.Spider):
    name = "family_links"

    def start_requests(self):
        xml_url = "https://norelem.de/sitemap/en-de.xml"
        xml_page = requests.get(xml_url)
        soup = BeautifulSoup(xml_page.content, "xml")

        re_pattern = re.compile(r"^http.+/p/agid.\d+")
        urls = []
        for url in soup.find_all("loc"):
            if re_pattern.match(url.text):
                urls.append(url.text)

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "proxy": "http://168.228.47.129:9197:PHchyV:qvzX3m",
                },
            )

    def parse(self, response):
        # options = webdriver.ChromeOptions()
        # # options.add_argument("--headless=new")
        # browser = webdriver.Chrome(options=options)
        browser = webdriver.Chrome()

        if response.css("button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"):
            click_cookie_bot(browser, response.url)

        table = False
        start = time.time()
        while table is False:
            for i in range(10):
                ActionChains(browser).scroll_by_amount(0, i).perform()
            try:
                table = WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "div.product-table a[data-id]",
                        )
                    )
                )
            except TimeoutException:
                if (time.time() - start) < 150:
                    pass
                else:
                    break

        a_tags = browser.find_elements(
            By.CSS_SELECTOR, "div.product-table a[data-id][href]"
        )
        browser.quit()
        links = [a.get_attribute("href") for a in a_tags]

        for link in links:
            yield {"product_links": link, "family_links": response.url}
