import csv
from pathlib import Path
from bs4 import BeautifulSoup
import scrapy
from tabulate import tabulate


CURRENT_DIR = Path("__file__").resolve()
BASE_DIR = CURRENT_DIR.parent
RESULTS_DIR = BASE_DIR / "results"
LINKS_DIR = BASE_DIR / "links"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"


def del_classes_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th", "target", "itemprop", "content"]:
            del tag[attribute]

    return str(soup)


def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(["class", "style", "id", "scope", "data-th", "target"]):
        data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


def create_html_table(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    res = []
    divs = soup.find_all("div")
    for div in divs:
        span_list = div.find_all("span")
        if len(span_list) == 2:
            res.append(i.text.strip() for i in span_list)
    # spans = soup.find_all("span")
    # for i in range(0, len(spans), 2):
    #     res.append((spans[i].text.strip(), spans[i + 1].text.strip()))

    html = tabulate(res, tablefmt="html").replace("\n", "")

    return html


def save_error(url, error, field, err_file_path=ERRORS_FILENAME, *args, **kwargs):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


class ArmaturenSpider(scrapy.Spider):
    name = "armaturen"

    custom_settings = {
        # "CONCURRENT_REQUESTS": 30,
        "RETRY_TIMES": 3,
        "DUPEFILTER_DEBUG": True,
        # "ROBOTSTXT_OBEY": False,
    }

    def start_requests(self):

        urls = []

        # with open(LINKS_DIR / "shop.ms-armaturen.com_all_links.csv") as csvfile:
        with open("/home/sana451/PycharmProjects/scrapy_parsers/shop_ms_armaturen_com/links/armaturen_links.csv") as csvfile:

            reader = csv.reader(csvfile)
            urls = list(reader)[1:]

        for url in urls:
            yield scrapy.Request(url=url[0], callback=self.parse, errback=self.errback)

    def parse(self, response):
        result = dict()

        try:
            field_name = "url"
            result[field_name] = response.url
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Заголовок"
            # inspect_response(response, self)
            result[field_name] = response.css("h1::text").get().strip()
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Артикул"
            # inspect_response(response, self)
            article = response.css(".product-detail-ordernumber::text").get()
            if article:
                result[field_name] = article.strip()
            else:
                result[field_name] = ""
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Version (модель)"
            # inspect_response(response, self)
            version = response.xpath("//span[contains(text(), 'version')]/..").css(".properties-value::text").get()
            if version:
                result[field_name] = version.strip()
            else:
                result[field_name] = ""
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Производитель"
            # inspect_response(response, self)
            manufacturer = response.css(".twt-product-detail-manufacturer::text").get()
            if manufacturer:
                result[field_name] = manufacturer.strip()
            else:
                result[field_name] = ""
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Характеристики"
            # inspect_response(response, self)
            description = response.css("div.product-detail-properties-text").get()
            if not description:
                description = response.css("div.order-nr-wrap").get()
            if description:
                description = del_classes_from_html(description)
                description = create_html_table(description)
                result[field_name] = description
            else:
                result[field_name] = ""
        except Exception as error:
            save_error(response.url, error, field_name)
        #
        try:
            field_name = "Вес"
            # inspect_response(response, self)
            weight = response.css(".twt-product-detail-weight::text").get()
            if weight:
                result[field_name] = weight.strip()
            else:
                result[field_name] = ""
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Картинки"
            # inspect_response(response, self)
            images = [img.attrib['data-src'] for img in response.css(".gallery-slider-thumbnails img[data-src]")]
            if images:
                result[field_name] = " | ".join(images)
            else:
                result[field_name] = ""
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Цена"
            # inspect_response(response, self)
            price = response.css(".product-detail-price::text").get()
            if price:
                result[field_name] = price.strip().lstrip("Catalog price: €").rstrip("*")
            else:
                result[field_name] = ""
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Наличие"
            # inspect_response(response, self)
            availability = response.css(".product-detail-delivery-information p::text").get()
            if availability:
                result[field_name] = availability.strip()
            else:
                result[field_name] = ""
        except Exception as error:
            save_error(response.url, error, field_name)

        #
        # try:
        #     field_name = "Категории"
        #     # inspect_response(response, self)
        #     categories = [i.attrib['title'] for i in response.css("div.breadcrumbs li a")][2:]
        #     result[field_name] = " > ".join(categories)
        # except Exception as error:
        #     save_error(response.url, error, field_name)

        yield result

    async def errback(self, failure):
        save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")

# from industriation_ru.spiders.link_spyder import *
