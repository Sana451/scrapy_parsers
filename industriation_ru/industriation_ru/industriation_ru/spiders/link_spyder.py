import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import scrapy
from scrapy.shell import inspect_response
from tabulate import tabulate

SITEMAP_URL = "https://industriation.ru/sitemap/"

BASE_DIR = Path("__file__").resolve().parent
RESULTS_DIR = BASE_DIR / "results"
LINKS_DIR = BASE_DIR / "links"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"

SITE_DOMAIN = "https://industriation.ru"


def del_classes_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th", "target"]:
            del tag[attribute]

    return str(soup)


def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(["class", "style", "id", "scope", "data-th", "target"]):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


def create_html_table(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    #     for tag in soup():
    #         for attribute in ["class"]:
    #             del tag[attribute]
    res = []
    for span in soup.find_all("span"):
        res.append((span.text, span.findNext().text))

    html = tabulate(res, tablefmt="html").replace("\n", "")

    return html


def save_error(url, error, field, err_file_path=ERRORS_FILENAME):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


class LinkSpider(scrapy.Spider):
    name = "industriation"

    custom_settings = {
        "CONCURRENT_REQUESTS": 30,
        "RETRY_TIMES": 3,
        "DUPEFILTER_DEBUG": True,
        "ROBOTSTXT_OBEY": False, }

    # re_pattern = re.compile(r"^http.+/p/agid.\d+")
    def start_requests(self):
        """
        Раскомментировать до строки writer.writerow([link]), в случае необходимости анализировать весь сайт.
        """
        # soup = BeautifulSoup(requests.get(SITEMAP_URL).content, "xml")
        # sitemap_list = [loc.text for loc in soup.find_all("loc") if "aproduct" in loc.text]
        #
        urls = []

        if Path(LINKS_DIR / "links.csv").exists():
            with (LINKS_DIR / "links.csv").open("r") as links_csv_file:
                links = links_csv_file.readlines()
                if len(links) > 0:
                    urls = links
        # else:
        #     for sitemap in sitemap_list:
        #         product_soup = BeautifulSoup(requests.get(sitemap).content, "xml")
        #         product_list = [loc.text for loc in product_soup.find_all("loc")]
        #         urls.extend(product_list)
        #         with open(LINKS_DIR / "links.csv", "a") as link_file:
        #             writer = csv.writer(link_file)
        #             for link in product_list:
        #                 writer.writerow([link])

        else:
            only_AirTac_products = [f"https://industriation.ru/search/?search=AirTac&page={i}" for i in range(202)]

            for group_link in only_AirTac_products:
                group_link_soup = BeautifulSoup(requests.get(group_link).content)
                airtag_links = [a["href"] for a in group_link_soup.select("div.product-card div.name a")]
                urls.extend(airtag_links)
                with open(LINKS_DIR / "links.csv", "a") as link_file:
                    writer = csv.writer(link_file)
                    for link in airtag_links:
                        writer.writerow([link])

        for url in urls:
            # yield scrapy.Request(url=url.strip(), callback=self.parse)  # для всего сайта
            yield scrapy.Request(url=url, callback=self.parse)

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
            result[field_name] = response.css("h1.heading-title::text").get()
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Артикул"
            # inspect_response(response, self)
            result[field_name] = response.xpath("//div[contains(text(), 'Артикул')]").css("span::text").get()
        except Exception as error:
            save_error(response.url, error, field_name)

        description_soup = BeautifulSoup(response.css("div#description").get())

        try:
            field_name = "Производитель"
            # inspect_response(response, self)
            try:
                manufacturer = [i for i in description_soup.select(".row") if field_name in i.text][0].find_all("div")[
                    1].text.strip()
                result[field_name] = manufacturer
            except IndexError:
                result[field_name] = ""
                # save_error(response.url, error, field_name)
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Наименование"
            # inspect_response(response, self)
            try:
                designation = [i for i in description_soup.select(".row") if field_name in i.text][0].find_all("div")[
                    1].text.strip()
                result[field_name] = designation
            except IndexError:
                result[field_name] = ""
                # save_error(response.url, error, field_name)
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Тип оборудования"
            # inspect_response(response, self)
            try:
                equipment_type = \
                    [i for i in description_soup.select(".row") if field_name in i.text][0].find_all("div")[
                        1].text.strip()
                result[field_name] = equipment_type
            except IndexError:
                result[field_name] = ""
                # save_error(response.url, error, field_name)
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Технические характеристики"
            # inspect_response(response, self)
            copy_description_soup = description_soup
            body = copy_description_soup.find("body").find("div")
            body.select_one("div.mini-text").extract()
            body = del_classes_from_html(str(body))
            body = create_html_table(str(body))
            result[field_name] = body
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Вес"
            # inspect_response(response, self)
            try:
                weight = \
                    [i for i in description_soup.select(".row") if field_name in i.text][0].find_all("div")[
                        1].text.strip()
                result[field_name] = weight
            except IndexError:
                result[field_name] = ""
                # save_error(response.url, error, field_name)
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Картинки"
            # inspect_response(response, self)
            main_image = response.css("div#images img.image").attrib['src']
            other_images = response.xpath("//img[@data-zoom]")[1:]
            if not other_images:
                result[field_name] = main_image
            else:
                zoom_images = [img.attrib['data-zoom'] for img in other_images]
                result[field_name] = " | ".join([main_image] + zoom_images)
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Цена"
            # inspect_response(response, self)
            price = response.css("div.price::text").get()
            if price:
                result[field_name] = price.strip("₽")
            else:
                result[field_name] = ""
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "PDF"
            # inspect_response(response, self)
            pdf = [SITE_DOMAIN + link.attrib['data-file'] for link in response.css("div.file") if
                   "series_group-docs" in link.attrib['data-file']]
            result[field_name] = " | ".join(pdf)
        except Exception as error:
            save_error(response.url, error, field_name)

        try:
            field_name = "Категории"
            # inspect_response(response, self)
            categories = [i.attrib['title'] for i in response.css("div.breadcrumbs li a")][2:]
            result[field_name] = " > ".join(categories)
        except Exception as error:
            save_error(response.url, error, field_name)

        yield result

# from industriation_ru.spiders.link_spyder import *
