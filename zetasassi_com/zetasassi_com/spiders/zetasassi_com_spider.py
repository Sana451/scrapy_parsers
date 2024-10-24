import csv
import sys

from parsel import Selector
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


class ZetasassiComSpiderSpider(scrapy.Spider):
    name = "zetasassi_com_spider"
    allowed_domains = ["zetasassi.com"]

    def start_requests(self):
        with open(RESULTS_DIR / "zetasassi.com.links.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            start_urls = [row[0] for row in list(reader)[1:]]
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                )

    def parse(self, response):
        result = dict()

        result["url"] = response.url

        try:
            field = "Заголовок"
            title = response.xpath("//form//h1[@itemprop='name']//text()").get()
            if title:
                result[field] = title.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Краткое описание"
            short_description = response.css(".short-description::text").get()
            if short_description:
                result[field] = short_description.strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Описание"
            description = response.css(".long-description span::text")
            if description:
                result[field] = description[0].get().strip()
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            images = response.css("#design-product-thumbnails li a")
            if images:
                result[field] = " | ".join([a.attrib['href'] for a in images])
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            cats = response.css(".breadcrumbs li span::text").getall()
            if cats:
                result[field] = " > ".join(cats)
            else:
                result[field] = ""
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        items = response.css(".item")

        for item in items:
            item = Selector(item.get())

            try:
                field = "SKU"
                sku = item.xpath("//p[@itemprop='sku']//text()").get()
                if sku:
                    result[field] = sku.strip()
                else:
                    result[field] = ""

            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Цена"
                price = item.xpath("//div[@class='price']//text()").get()
                if price:
                    result[field] = price.replace("€", "").strip()
                else:
                    result[field] = ""

            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Наличие"
                avail = item.xpath("//div[@class='sku']/p[@align='right']//text()").get()
                if avail:
                    result[field] = avail.strip()
                else:
                    result[field] = ""

            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "Доставка"
                delivery = item.xpath("//div[@class='sku']//p[not(@align) and not(@itemprop)]//text()").get()
                if delivery:
                    result[field] = delivery.strip()
                else:
                    result[field] = ""

            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field ="Характеристики"
                details = item.xpath("//div[@class='option']")
                if details:
                    details = [[i.strip() for i in sel.css("::text").getall()[1:]] for sel in details]
                    result[field] = tabulate(details, tablefmt="html")
                else:
                    result[field] = ""
            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            # try:
            #     field = "Newton"
            #     newton = item.xpath("//div[@class='option' and (contains(., 'NEWTON'))]//text()").getall()
            #     if newton:
            #         result[field] = newton[-1].strip()
            #
            #     else:
            #         result[field] = ""
            #
            # except Exception as error:
            #     result[field] = ""
            #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
            #
            # try:
            #     field = "Pulley"
            #     pulley = item.xpath("//div[@class='option' and (contains(., 'PULLEY'))]//text()").getall()
            #     if pulley:
            #         result[field] = pulley[-1].strip()
            #     else:
            #         result[field] = ""
            #
            # except Exception as error:
            #     result[field] = ""
            #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
            #
            # try:
            #     field = "Материал"
            #     material = item.xpath("//div[@class='option' and (contains(., 'MATERIAL'))]//text()").getall()
            #     if material:
            #         result[field] = material[-1].strip()
            #     else:
            #         result[field] = ""
            #
            # except Exception as error:
            #     result[field] = ""
            #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
            #
            # try:
            #     field = "Lever"
            #     lever = item.xpath("//div[@class='option' and (contains(., 'LEVER'))]//text()").getall()
            #     if lever:
            #         result[field] = lever[-1].strip()
            #     else:
            #         result[field] = ""
            #
            # except Exception as error:
            #     result[field] = ""
            #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
            #
            # try:
            #     field = "Chain"
            #     chain = item.xpath("//div[@class='option' and (contains(., 'CHAIN'))]//text()").getall()
            #     if chain:
            #         result[field] = chain[-1].strip()
            #     else:
            #         result[field] = ""
            #
            # except Exception as error:
            #     result[field] = ""
            #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
            #
            # try:
            #     field = "Sprocket"
            #     sprocket = item.xpath("//div[@class='option' and (contains(., 'SPROCKET'))]//text()").getall()
            #     if sprocket:
            #         result[field] = sprocket[-1].strip()
            #     else:
            #         result[field] = ""
            #
            # except Exception as error:
            #     result[field] = ""
            #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
            #
            # try:
            #     field = "Type"
            #     type = item.xpath("//div[@class='option' and (contains(., 'TYPE'))]//text()").getall()
            #     if type:
            #         result[field] = type[-1].strip()
            #     else:
            #         result[field] = ""
            #
            # except Exception as error:
            #     result[field] = ""
            #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
            #
            # try:
            #     field = "Thread"
            #     thread = item.xpath("//div[@class='option' and (contains(., 'THREAD'))]//text()").getall()
            #     if thread:
            #         result[field] = thread[-1].strip()
            #     else:
            #         result[field] = ""
            #
            # except Exception as error:
            #     result[field] = ""
            #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
            #
            # try:
            #     field = "Length"
            #     length = item.xpath("//div[@class='option' and (contains(., 'LENGTH'))]//text()").getall()
            #     if length:
            #         result[field] = length[-1].strip()
            #     else:
            #         result[field] = ""
            #
            # except Exception as error:
            #     result[field] = ""
            #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
            #
            # try:
            #     field = "Color"
            #     color = item.xpath("//div[@class='option' and (contains(., 'COLOUR'))]//text()").getall()
            #     if color:
            #         result[field] = color[-1].strip()
            #     else:
            #         result[field] = ""
            #
            # except Exception as error:
            #     result[field] = ""
            #     my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            try:
                field = "PDF"
                pdf = item.xpath("//a[contains(text(), 'pdf')]//@href").get()
                if pdf:
                    result[field] = pdf.strip()
                else:
                    result[field] = ""

            except Exception as error:
                result[field] = ""
                my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

            yield result
