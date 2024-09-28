import csv
import json
import sys

import requests
from tabulate import tabulate

sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
from tools import my_scraping_tools as my_tools
from bs4 import BeautifulSoup

from pathlib import Path

import scrapy

BASE_DIR = Path("__file__").resolve().parent
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


class RiederSpiderSpider(scrapy.Spider):
    name = "rieder_spider"
    allowed_domains = ["riegler.de"]

    def start_requests(self):
        with open(RESULTS_DIR / "riegler_links2.csv", "r") as links_file:
            reader = csv.reader(links_file)
            start_urls = list(reader)

        for url in start_urls:
            yield scrapy.Request(url=url[0],
                                 callback=self.parse,
                                 )

    def parse(self, response):
        links = [a.attrib["href"] for a in response.css("div.customer-menu a")]
        if "https://www.riegler.de/de/de/customer/account/logout" in links:
            self.log("!!!!!!!!!!! {not authorized} !!!!!!!!!!!!")

        result = dict()

        if not response.css("div.product-info-main"):
            return

        result["url"] = response.url

        try:
            field = "Заголовок"
            title = response.css("h1.page-title span::text").get()
            result[field] = title
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            article = response.css("div[itemprop=sku]::text").get()
            result[field] = article
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Type number"
            type_num = response.css("div.type-no div[itemprop=type-no]::text").get()
            result[field] = type_num
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            product_id = int(
                response.css("div.product-info-main div.price-final_price").attrib["data-product-id"].strip()
            )
            js_api_res = make_post_for_price(product_id)
        except Exception as error:
            my_tools.save_error(response.url, error, "Product id not found", ERRORS_FILENAME)

        try:
            field = "Цена"
            # price = response.css("div.product-info-price span.price-value[data-role='price-gross']::text").get()
            # result[field] = price.rstrip("€")
            price = js_api_res["full_price"]
            result[field] = price
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена со скидкой"
            sale_price = js_api_res["sale_price"]
            result[field] = sale_price
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Наличие"
            availabillity = js_api_res["avalabillity"]
            result[field] = availabillity
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            main_image = response.css("img[alt='main product photo']").attrib["src"]
            # images = response.css("div.fotorama div[href]")
            result[field] = main_image
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "PDF"
            pdf_links = response.css("a.download-link")
            pdf = [link.attrib["href"] for link in pdf_links if ".pdf" in link.attrib["href"]]
            result[field] = " | ".join(pdf)
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Краткое описание"
            description = response.css("div.product-description::text").get()
            result[field] = description
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Характеристики"
            divs = response.css("div.product-attributes .attribute")
            details_clean = [my_tools.del_classes_from_html(div.get()) for div in divs]

            clean_table_rows = []
            for detail in details_clean:
                soup = BeautifulSoup(detail, "html.parser")
                label = soup.select("div")[1].text
                value = soup.select("div")[2].text
                clean_table_rows.append((label, value))
            details_table = tabulate(clean_table_rows, tablefmt="html").replace("\n", "")
            result[field] = details_table
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            script_selector = response.xpath("//script[contains(text(), 'breadcrumbs')]").css("::text").get()
            json_from_script = json.loads(script_selector)
            categories = " > ".join(
                json_from_script[".breadcrumbs"]["breadcrumbs"]["categories"][-1]["link"].lstrip(
                    "https://www.riegler.de/de/de/").rstrip(
                    ".html").split("/"))
            result[field] = categories
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result


def make_post_for_price(product_id: int):
    resp = requests.post("https://www.riegler.de/de/de/erp/reload/data/",
                         data=f'products%5B4%5D%5BproductId%5D={product_id}&form_key=o6yviFzaTLqAbn0R',
                         headers={
                             "accept": "*/*",
                             "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                             "priority": "u=1, i",
                             "referer": "https://www.riegler.de/de/de/filter-futura-mit-pc-behalter-schutzkorb-5-m-bg-4-g-1-ha-100150-2.html",
                             "sec-fetch-dest": "empty",
                             "sec-fetch-mode": "cors",
                             "sec-fetch-site": "same-origin",
                             "x-requested-with": "XMLHttpRequest"
                         },
                         cookies={
                             "PHPSESSID": "ui87dafqnnlof8j3130uqhslj9",
                             "STUID": "416af0d2-bbf8-13a4-9b04-04ff3f060040",
                             "STVID": "e65cdae2-7f49-fd3e-ffcb-21c5a74b875a",
                             "X-Magento-Vary": "5419d2091fac5275c00341aef91aff418768e5c0",
                             "_gcl_au": "1.1.813304060.1727181128",
                             "form_key": "o6yviFzaTLqAbn0R",
                             "mage-banners-cache-storage": "{}",
                             "mage-cache-sessid": "true",
                             "mage-cache-storage": "{}",
                             "mage-cache-storage-section-invalidation": "{}",
                             "mage-messages": "",
                             "persistent_shopping_cart": "uj3dn1UxTyMtBsI2mvVQqldVPmIDAkt46WPqU1whagqDiWs9sK",
                             "private_content_version": "3e23049cb34477fab9d8097b978d1601",
                             "product_data_storage": "{}",
                             "recently_compared_product": "{}",
                             "recently_compared_product_previous": "{}",
                             "recently_viewed_product": "{}",
                             "recently_viewed_product_previous": "{}",
                             "section_data_ids": "{%22company%22:1727245621%2C%22requisition%22:1727245621%2C%22customer-product-data%22:1727247607%2C%22customer%22:1727245607%2C%22compare-products%22:1727245607%2C%22last-ordered-items%22:1727245607%2C%22cart%22:1727245621%2C%22directory-data%22:1727245607%2C%22captcha%22:1727245607%2C%22wishlist%22:1727245607%2C%22company_authorization%22:1727245607%2C%22negotiable_quote%22:1727245607%2C%22instant-purchase%22:1727245607%2C%22loggedAsCustomer%22:1727245607%2C%22multiplewishlist%22:1727245607%2C%22purchase_order%22:1727245607%2C%22persistent%22:1727245607%2C%22review%22:1727245607%2C%22webforms%22:1727245607%2C%22contact-person%22:1727245607%2C%22recently_viewed_product%22:1727245607%2C%22recently_compared_product%22:1727245607%2C%22product_data_storage%22:1727245607%2C%22paypal-billing-agreement%22:1727245607}",
                             "uslk_umm_121658_s": "ewAiAHYAZQByAHMAaQBvAG4AIgA6ACIAMQAiACwAIgBkAGEAdABhACIAOgB7AH0AfQA="
                         },
                         auth=(),
                         )

    js_res = resp.json()[0]
    res = {"sale_price": js_res["NetValue"],
           "avalabillity": js_res["main_stock_message"],
           "full_price": js_res["GrossPrice"]}
    return res
