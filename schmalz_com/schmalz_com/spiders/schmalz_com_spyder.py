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


class SchmalzComSpyderSpider(scrapy.Spider):
    name = "schmalz_com_spyder"
    allowed_domains = ["schmalz.com"]

    def start_requests(self):
        with open(RESULTS_DIR / "schmalz.com.links.csv", "r", encoding="utf-8") as links_csv_file:
            reader = csv.reader(links_csv_file)
            start_urls = [row[0] for row in list(reader)]
            for url in start_urls[:]:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse
                )

    def parse(self, response):
        result = {"url": response.url}

        try:
            field = "Заголовок"
            result[field] = response.css("h1 span::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Артикул"
            result[field] = response.xpath("//*[@data-qa-id='pdp_part_number_span']//span[2]//text()").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "SKU"
            result[field] = response.xpath("//input[@name='sku']").attrib["value"]
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Модель"
            result[field] = response.css(".pdp__description span::text").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Цена"
            result[field] = get_price_by_sku(result["SKU"])
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            availability_json = get_availability_by_sku(result["SKU"])

            try:
                field = "Наличие"
                result[field] = availability_json["availabilityStatus"].replace("PRODUCT_AVAILABLE_STATUS_", "")
            except Exception:
                result[field] = ""
            try:
                field = "Общая стоимость"
                result[field] = availability_json["price"].replace("€", "")
            except Exception:
                result[field] = ""
            try:
                field = "Дата отправки"
                result[field] = availability_json["stock"][0]["deliveryDate"]
            except Exception:
                result[field] = ""
            try:
                field = "Количество"
                result[field] = availability_json["stock"][0]["quantity"]
            except Exception:
                result[field] = ""
        except Exception as error:
            my_tools.save_error(response.url, error, "Availabillity", ERRORS_FILENAME)

        try:
            field = "Картинки"
            main_image = response.css(".active img")
            if main_image:
                main_image = main_image.attrib["src"]
            else:
                main_image = ""
            second_image = response.css(".pdp__details img.d-block")
            if second_image:
                second_image = second_image.attrib["src"]
            else:
                second_image = ""
            if main_image and second_image:
                result[field] = " | ".join([main_image, second_image])
            elif main_image:
                result[field] = main_image
            elif second_image:
                result[field] = second_image
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "PDF"
            DOMAIN = "https://www.schmalz.com"
            pdf = response.xpath("//*[@data-qa-id='product_sheet_link']").attrib["href"]
            result[field] = f"{DOMAIN}/{pdf}"
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Вес"
            result[field] = response.xpath("//tr[contains(., 'Gewicht')]//td[2]//text()").get().strip()
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Краткое описание"
            description = response.xpath("//*[@data-qa-id='product_details_section_pdp']//table").get()
            result[field] = my_tools.del_classes_from_html(description)
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Проектные данные"
            project_data = response.xpath("//tr[@class='typ-main-productlabel']/ancestor::table")
            project_data = project_data[0].get()
            result[field] = my_tools.del_classes_from_html(project_data)
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Технические характеристики"
            tech_data = response.xpath("//tr[@class='typ-main-productlabel']/ancestor::table")
            tech_data = tech_data[1].get()
            result[field] = my_tools.del_classes_from_html(tech_data)
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        try:
            field = "Категории"
            categories = response.xpath("//*[@class='breadcrumbs']//a//span")
            cats = " > ".join([span.css("::text").get() for span in categories][1:])
            result[field] = cats
        except Exception as error:
            result[field] = ""
            my_tools.save_error(response.url, error, field, ERRORS_FILENAME)

        yield result


def get_price_by_sku(sku: str):
    response = requests.get(f"https://www.schmalz.com/de-de/product-permissions?sku={sku}",
                            headers={
                                "accept": "application/json, text/javascript, */*; q=0.01",
                                "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
                                "cache-control": "no-cache",
                                "pragma": "no-cache",
                                "priority": "u=0, i",
                                "referer": "https://www.schmalz.com/de-de/vakuumtechnik-fuer-die-automation/vakuum-komponenten/vakuum-sauggreifer/zubehoer-vakuum-sauggreifer/saugereinsaetze-spi-fuer-spb2-305924/10.01.06.04044/",
                                "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
                                "sec-ch-ua-mobile": "?0",
                                "sec-ch-ua-platform": "\"Linux\"",
                                "sec-fetch-dest": "empty",
                                "sec-fetch-mode": "cors",
                                "sec-fetch-site": "same-origin",
                                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                                "x-requested-with": "XMLHttpRequest"
                            },
                            cookies={
                                "AWSALB": "tGO2iDj7rHTQXEp8pk1CdI1peuzrejGbFzhuCQmIRusodD5A8XIvqAReYn6+GBjS80VR1fVIC0nTJqqH5ZQegtNEaO8NqKGEoF4fcnTpDFI1wMtFiVVf9Ac6kTeq",
                                "AWSALBCORS": "tGO2iDj7rHTQXEp8pk1CdI1peuzrejGbFzhuCQmIRusodD5A8XIvqAReYn6+GBjS80VR1fVIC0nTJqqH5ZQegtNEaO8NqKGEoF4fcnTpDFI1wMtFiVVf9Ac6kTeq",
                                "AWSELB": "E97BF37114DC14F0AEB705612B29CF3F419B2BFF25D43631D3B1C9B9BD85111F0FFB83163FB61F484404597DA1F3B411DD66ED14092FF07038EF70EBF5D28FC4CA384C8708CDE678430BEA35DE1C27FD5E5336BEA8",
                                "JSESSIONID": "E83AD63007860BF02A4BE35177B66038",
                                "OAuth_Token_Request_State": "61c68f02-e0be-4044-9491-2ea88ec21546",
                                "_clck": "11aqexd%7C2%7Cfpn%7C0%7C1735",
                                "_clsk": "hxrfnn%7C1727770774284%7C10%7C1%7Cp.clarity.ms%2Fcollect",
                                "_uetsid": "c01184a07fc711ef9bb09714495b5495",
                                "_uetvid": "c0119ae07fc711ef9ae6652693cba2ca",
                                "channelKeyCookie": "web-DE",
                                "cmsSiteIdCookie": "de-de",
                                "cmsSiteIdCookieOrigin": "Deutschland",
                                "countrySelector": "DE",
                                "localeCookie": "de",
                                "loggedIn": "true"
                            },
                            auth=(),
                            )
    return response.json()["price"].replace("€", "")


def get_availability_by_sku(sku: str):
    response = requests.get(f"https://www.schmalz.com/de-de/productAvailability?quantity=1&sku={sku}",
                            headers={
                                "accept": "application/json, text/javascript, */*; q=0.01",
                                "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
                                "cache-control": "no-cache",
                                "pragma": "no-cache",
                                "priority": "u=0, i",
                                "referer": "https://www.schmalz.com/de-de/vakuumtechnik-fuer-die-automation/vakuum-komponenten/vakuum-sauggreifer/zubehoer-vakuum-sauggreifer/saugereinsaetze-spi-fuer-spb2-305924/10.01.06.04044/",
                                "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
                                "sec-ch-ua-mobile": "?0",
                                "sec-ch-ua-platform": "\"Linux\"",
                                "sec-fetch-dest": "empty",
                                "sec-fetch-mode": "cors",
                                "sec-fetch-site": "same-origin",
                                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                                "x-requested-with": "XMLHttpRequest"
                            },
                            cookies={
                                "AWSALB": "tGO2iDj7rHTQXEp8pk1CdI1peuzrejGbFzhuCQmIRusodD5A8XIvqAReYn6+GBjS80VR1fVIC0nTJqqH5ZQegtNEaO8NqKGEoF4fcnTpDFI1wMtFiVVf9Ac6kTeq",
                                "AWSALBCORS": "tGO2iDj7rHTQXEp8pk1CdI1peuzrejGbFzhuCQmIRusodD5A8XIvqAReYn6+GBjS80VR1fVIC0nTJqqH5ZQegtNEaO8NqKGEoF4fcnTpDFI1wMtFiVVf9Ac6kTeq",
                                "AWSELB": "E97BF37114DC14F0AEB705612B29CF3F419B2BFF25D43631D3B1C9B9BD85111F0FFB83163FB61F484404597DA1F3B411DD66ED14092FF07038EF70EBF5D28FC4CA384C8708CDE678430BEA35DE1C27FD5E5336BEA8",
                                "JSESSIONID": "E83AD63007860BF02A4BE35177B66038",
                                "OAuth_Token_Request_State": "61c68f02-e0be-4044-9491-2ea88ec21546",
                                "_clck": "11aqexd%7C2%7Cfpn%7C0%7C1735",
                                "_clsk": "hxrfnn%7C1727770774284%7C10%7C1%7Cp.clarity.ms%2Fcollect",
                                "_uetsid": "c01184a07fc711ef9bb09714495b5495",
                                "_uetvid": "c0119ae07fc711ef9ae6652693cba2ca",
                                "channelKeyCookie": "web-DE",
                                "cmsSiteIdCookie": "de-de",
                                "cmsSiteIdCookieOrigin": "Deutschland",
                                "countrySelector": "DE",
                                "localeCookie": "de",
                                "loggedIn": "true"
                            },
                            auth=(),
                            )
    return response.json()
