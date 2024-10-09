import csv
import json
import sys

import requests
from bs4 import BeautifulSoup
from scrapy import Request
from tabulate import tabulate

sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
from tools import my_scraping_tools as my_tools  # from bs4 import BeautifulSoup

from pathlib import Path

import scrapy
from urllib.parse import urlencode, quote_plus

BASE_DIR = Path("__file__").resolve().parent
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://air-com.pl/p/series-a-directly-operated-solenoid-valves,38472,866195?__cf_chl_tk=Pf3F_tSDeF44XgqHd5vioY5n52RUgraRh7Oi4rm_LaY-1728237858-0.0.1.1-15487",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"127.0.6533.119\"",
    "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"127.0.6533.119\", \"Chromium\";v=\"127.0.6533.119\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-ch-ua-platform-version": "\"6.8.0\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

cookies = {
    "_gcl_au": "1.1.207607264.1728229905",
    "_ga": "GA1.2.1284376541.1728229895",
    "_gid": "GA1.2.1016951847.1728229905",
    "CookieConsent": "{stamp:%27eHD+icLMBpWfhTlFNb0MXok0o/rN/u8SL7vIwrsIg9y0YYUKsdcr+w==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:1%2Cutc:1728300373487%2Cregion:%27ru%27}",
    "_uetsid": "e36c902083fa11ef82b1ed9a9030b87e",
    "_uetvid": "e36cc17083fa11ef990bbbbb6c1c1f90",
    "_clck": "1fwgahq%7C2%7Cfpu%7C0%7C1739",
    "_clsk": "1kjlvxq%7C1728363614742%7C1%7C1%7Cp.clarity.ms%2Fcollect",
    "cf_clearance": "qU3qF9gvyJZK5w7g5LID3zMsfDwvXekfAz.x7pmb2ws-1728363615-1.2.1.1-PO8DjOpdZODNMBsRDXlG1L0j9VrwxY47526g2CKCoLX.SKdvKNbi8qqrpaFgczSsVDBPFuntr5d9qc47UlgPHtmCHuwWNnLy1fVqsjcUl3MS4lTrw_0SP85iLIFMPfBuDb5MJ87TRVBQnMCMjXkqx4tfx10De9n2z.YOHzKbzfaW7X0Wo6l3YX3ZftEgOC_duhpQDFO_pAHu2Sca2daeAo988YmGs0Wi06KCoaoPaqBj6zc0Hu3n5tD6iZMHJ_Tw20vs3wQ0Dr7ZqYXEkRtOKZachiJ_.j1XFHpQk8XGjRf4VG.loMr681BB3NxX07g.J9_YzbOZ7VDRh4MULLUEBEOyb5AHI9vh8wM57hQkG4BcIUP80dIxGO5ZQa8_r9BlBM2DtMzelnlPYhAw_zRGuf6pyWjnpfJWcJjX2AABBWY",
    "user_session": "eyJpdiI6IkovaFVpQ2cvbll2QXRhSUV4cGVNUEE9PSIsInZhbHVlIjoiZ1RBUThkU0NvOW9tL1ljUFpLS08wMklOdEpnZDNnd1dpNnhYcEF1VjZ0RUtha29VekZBSSs3SERkVDY2YnZabllIUWs4bFUzSERDaStOeEdMQzlNbHNpcXJDUHpIMzVYTnViUU13ZUQyNXpVR0dUK3RNNFR6d2E1RjNUTi9LUEIiLCJtYWMiOiJmMmQ4Y2JhYzJjZjc2ZmJlYTY1ZGQ5YmZmNTU4YjcyOTVkNDY1OWE0MmRmOGIwYTAwY2Q5NTdhM2Q0N2JhNDYwIiwidGFnIjoiIn0%3D"
}


class AirComPlSpiderSpider(scrapy.Spider):
    name = "air_com_pl_spider"
    allowed_domains = ["air-com.pl", "zenrows.com"]

    def start_requests(self):
        with open(RESULTS_DIR / "air-com.pl.camozzi.links2.csv", "r", encoding="utf-8") as links_file:
            reader = csv.reader(links_file)
            start_urls = [url[0] for url in list(reader)]
            for url in start_urls[1:]:
                yield scrapy.Request(
                    url=url,
                    method='GET',
                    dont_filter=True,
                    cookies=cookies,
                    headers=headers,
                )

    def parse(self, response):
        result = dict()
        result["url"] = response.url

        try:
            field = "Заголовок"
            result[field] = response.css("span.title::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            result[field] = response.css("h2.product-signs-info span::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Код производителя"
            result[field] = response.xpath("//*[contains(text(), 'Kod prod')]//span//text()").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            result[field] = response.css(".price-current b::text").get().replace("zł", "").strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Наличие"
            result[field] = response.css(".product-ava-card span.product-ava::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        # try:
        #     field = ""
        #     delivery = response.css("//*[contains(text(), 'Wysyłka w')]").css("::text").get()
        #     result[field] = delivery.replace("Wysyłka w", "").strip()
        # except Exception as error:
        #     result[field] = ""
        #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
            
        try:
            field = "Отправка"
            result[field] = response.xpath(
                "//*[contains(@class, 'param-box-col')]//span[@class = 'sign']//b").css("::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            result[field] = response.css(".mainImage a[data-contener-main-image]").attrib["href"]
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Описание"
            desc = response.css("div.desc-content p::text").get()
            if not desc:
                desc = response.css("div.desc-content::text").get()

            result[field] = my_tools.del_classes_from_html(desc.strip())
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)


        try:
            field = "Характеристики"

            details = response.css("#accordion-tech .tech-content .tech-item").get()
            soup = BeautifulSoup(details, "html.parser")
            lst = [i.text.strip() for i in soup.select("div")[1:]]
            table_data = [(lst[i], lst[i + 1]) for i in range(0, len(lst), 2)]
            table = tabulate(table_data, tablefmt="html")
            result[field] = my_tools.del_classes_from_html(table)
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "PDF"
            result[field] = response.css("a.iconair-file-pdf").attrib["js-href"]
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)


        try:
            field = "Категории"
            cats = response.xpath("//ol[@itemscope]//li/a//span")
            cats = [cat.css("::text").get() for cat in cats][2:]
            result[field] = " > ".join(cats)
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result
