import csv
import sys

from tabulate import tabulate

if sys.platform == "linux":
    sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
elif sys.platform == "win32":
    sys.path.insert(0, r"D:\sana451\scrapy_parsers")
from tools import my_scraping_tools as my_tools

from pathlib import Path

import scrapy

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
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

cookies = {
    "mage-cache-storage": "{}",
    "mage-cache-storage-section-invalidation": "{}",
    "form_key": "24QE9ckcXZ3l7g6z",
    "recently_viewed_product": "{}",
    "recently_viewed_product_previous": "{}",
    "recently_compared_product": "{}",
    "recently_compared_product_previous": "{}",
    "product_data_storage": "{}",
    "_gcl_au": "1.1.1818661157.1729179733",
    "_clck": "1ly018h%7C2%7Cfq4%7C0%7C1751",
    "PHPSESSID": "4e9fvetdplgjnb64jqu83idmhn",
    "X-Magento-Vary": "f6a8d472cf7d9a5df1a8c798c8c87b3332afbbfcd9e3add7324afc2a703be2c1",
    "mage-cache-sessid": "true",
    "dont_show_login_message": "true",
    "private_content_version": "7f314c82423c831267076360560b1d4b",
    "section_data_ids": "{%22cart%22:1729233737%2C%22last-ordered-items%22:1729233737%2C%22customer%22:1729233737%2C%22compare-products%22:1729233737%2C%22directory-data%22:1729233737%2C%22captcha%22:1729233737%2C%22instant-purchase%22:1729233737%2C%22loggedAsCustomer%22:1729233737%2C%22persistent%22:1729233737%2C%22review%22:1729233737%2C%22wishlist%22:1729233737%2C%22seen-login-popup%22:1729233737%2C%22webforms%22:1729233737%2C%22crefopay%22:1729233737%2C%22recently_viewed_product%22:1729233737%2C%22recently_compared_product%22:1729233737%2C%22product_data_storage%22:1729233737%2C%22paypal-billing-agreement%22:1729233737%2C%22messages%22:1729236518}",
    "_clsk": "16capxj%7C1729237019476%7C69%7C1%7Cz.clarity.ms%2Fcollect"
}


class AceAceDeSpiderSpider(scrapy.Spider):
    name = "ace_ace_de_spider"
    allowed_domains = ["ace-ace.de"]

    def start_requests(self):
        with open(RESULTS_DIR / "ace-ace.de.links.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            start_urls = [row[0] for row in list(reader)[1:]]
            for url in start_urls[:]:
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

        if response.xpath("//a[contains(text(), 'Konfigurator')]"):
            with open(RESULTS_DIR / "configurator.csv", "a") as f:
                f.write("\n" + response.url)
            return

        if not response.css(".catmenu--products"):
            with open(RESULTS_DIR / "configurator.csv", "a", newline="") as f:
                f.write("\n" + response.url)
            return

        if not response.xpath("//tr[@class='active']"):
            with open(RESULTS_DIR / "configurator.csv", "a", newline="") as f:
                f.write("\n" + response.url)
            return

        try:
            field = "Заголовок"
            title = response.css("header h1::text").getall()
            if title:
                result[field] = title[0].strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            art = response.css("header h1::text").getall()
            if art:
                result[field] = art[1].strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Подзаголовок"
            sub_art = response.css("header h2::text").get()
            if sub_art:
                result[field] = sub_art.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            price = response.xpath("//meta[@itemprop='price']//@content").get()
            if price:
                result[field] = price.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Наличие"
            avail = response.css(".availability-info span::text").getall()
            if avail:
                result[field] = avail[0].strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Доставка"
            delivery = response.css(".availability-info span::text").getall()
            if delivery:
                result[field] = delivery[1].strip().lstrip("(").rstrip(")")
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "№ таможенного тарифа"
            tarifnum = response.xpath("//p[contains(., 'Zolltarifnummer')]//text()").getall()
            if tarifnum:
                result[field] = tarifnum[1]
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            images = response.xpath("//*[contains(@class, 'product-image')]//img//@src").getall()
            if images:
                result[field] = " | ".join([img for img in images if img.endswith(".jpg")])
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
        try:
            field = "PDF"
            pdf = response.xpath("//*[@class='download__item']//a//@href").get()
            if pdf:
                result[field] = pdf
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Вес"
            weight = response.xpath("//p[contains(., 'Gewicht')]//text()").getall()
            if weight:
                result[field] = weight[1]
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Краткое описание"
            short_desc = response.css("header h3::text").getall()
            if short_desc:
                result[field] = ". ".join(short_desc)
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Полное описание"
            desc = response.css(".category-description::text").getall()
            if desc:
                result[field] = "".join(desc).strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Характеристики"
            details = response.xpath("//*[contains(text(), 'Technische Daten')]//parent::div//table").get()
            if details:
                result[field] = my_tools.del_classes_from_html(details)
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Размеры"
            dimensions = response.css(".product-dimensions table").get()
            if dimensions:
                result[field] = my_tools.del_classes_from_html(dimensions)
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Коммерческая инф."
            commerce = response.css(".product-commercial p")
            if commerce:
                commerce = [("".join(a.css("::text").getall()[:-1]), a.css("::text").getall()[-1]) for a in commerce]
                result[field] = tabulate(commerce, tablefmt="html")
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            cats = response.url.split("/")
            if cats:
                result[field] = " > ".join(cats[5:-1])
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result
