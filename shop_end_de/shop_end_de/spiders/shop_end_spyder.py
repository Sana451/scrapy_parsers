import csv
import sys

from pathlib import Path
import scrapy

if sys.platform == "linux":
    sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
elif sys.platform == "win32":
    sys.path.insert(0, r"D:\sana451\scrapy_parsers")
from tools import my_scraping_tools as my_tools

BASE_DIR = Path("__file__").resolve().parent
RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


class ShopEndSpyderSpider(scrapy.Spider):
    name = "shop_end_spyder"

    # allowed_domains = ["shop.end.de"]

    def start_requests(self):
        with open(RESULTS_DIR / "shop.end.de.links.en.csv", "r", encoding="utf-8") as shop_end_links_file:
            reader = csv.reader(shop_end_links_file)
            start_urls = list(reader)
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url[0],
                    callback=self.parse,
                    meta={"playwright": True}
                )

    def parse(self, response):

        result = {"url": response.url}

        try:
            field = "Заголовок"
            title = response.css("#product-name::text").get()
            result[field] = title.strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            article = response.xpath("//*[@itemprop='sku']//text()").get()
            result[field] = article.strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            price = response.xpath("//*[@class='price block']//*[@class='price']//text()").get()
            result[field] = price.replace("€", "").strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Наличие"
            availability = response.xpath("//*[@data-unique-id='availability-info']//span[not(@class)]//text()").get()
            result[field] = availability.strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Картинки"
            image = response.xpath("//img[@itemprop='image']").attrib["src"]
            result[field] = image
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Характеристики"
            details = response.css("table.additional-attributes").get()
            details_cleaned = my_tools.del_classes_from_html(details)
            result[field] = details_cleaned
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Вес"
            weight = response.xpath("//tr[contains(., 'Gewicht')]//td//text()")
            unit_of_meas = response.xpath("//tr[contains(., 'Gewicht')]//td//@data-th").get()
            if not weight:
                weight = response.xpath("//tr[contains(., 'Weight')]//td//text()")
                unit_of_meas = response.xpath("//tr[contains(., 'Weight')]//td//@data-th").get()
            res = weight.get().strip() + unit_of_meas.replace(
                "Weight", "").replace("Gewicht", "").replace("[", "").replace("]", "")
            result[field] = res
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            categories = response.css("nav.breadcrumbs li a")
            cats_text = [cat.css("::text").get() for cat in categories]
            result[field] = " > ".join(cats_text[1:-1])
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result
