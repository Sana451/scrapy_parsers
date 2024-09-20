# import csv
# import re
# from pathlib import Path
#
# from bs4 import BeautifulSoup
#
# import scrapy
# from scrapy import FormRequest
# from scrapy.shell import inspect_response
# from tabulate import tabulate
#
# DOMAIN = "https://www.camlogic.it"
#
# BASE_DIR = Path("__file__").resolve().parent
#
# RESULTS_DIR = BASE_DIR / "results"
# ERRORS_DIR = BASE_DIR / "errors"
# ERRORS_FILENAME = ERRORS_DIR / "errors.csv"
#
#
# def del_classes_AND_divs_from_html(html: str) -> str:
#     soup = BeautifulSoup(html, "html.parser")
#     [d.decompose() for d in soup.find_all("div")]
#
#     for tag in soup():
#         for attribute in ["class", "style", "id", "scope", "data-th",
#                           "target", "itemprop", "content", "data-description", "data-uid",
#                           "data-name"]:
#             del tag[attribute]
#
#     result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
#     return result
#
#
# def del_classes_from_html(html: str) -> str:
#     soup = BeautifulSoup(html, "html.parser")
#
#     for tag in soup():
#         for attribute in ["class", "style", "id", "scope", "data-th",
#                           "target", "itemprop", "content", "data-description", "data-uid",
#                           "data-name", "href", "title"]:
#             del tag[attribute]
#
#     result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
#     return result
#
#
# def remove_tags(html):
#     soup = BeautifulSoup(html, "html.parser")
#     for data in soup(["class", "style", "id", "scope", "data-th", "target"]):
#         data.decompose()
#
#     return ' '.join(soup.stripped_strings)
#
#
# def create_html_table(html: str) -> str:
#     soup = BeautifulSoup(html, "html.parser")
#
#     res = []
#     divs = soup.find_all("div")
#     for div in divs:
#         span_list = div.find_all("span")
#         if len(span_list) == 2:
#             res.append(i.text.strip() for i in span_list)
#
#     html = tabulate(res, tablefmt="html").replace("\n", "")
#
#     return html
#
#
# def save_error(url, error, field, err_file_path=ERRORS_FILENAME):
#     with open(err_file_path, "a") as error_csvfile:
#         writer = csv.writer(error_csvfile)
#         writer.writerow([url, field, type(error), error])
#
#
# class TOCSpider(scrapy.Spider):
#     name = "camlogic_it_spyder"
#     allowed_domains = ["www.camlogic.it"]
#     domain_name = "demo.silverstripe.com"
#     start_urls = ['https://www.camlogic.it/en/login?redir=%2Fen%2Fuser']
#
#     def parse(self, response):
#         self.log(f"!!!!!!!!!!!!!parse,, {type(response)}")
#         self.log(response.css("form#customerSignInForm"))
#         self.log(response.url)
#         if response.xpath("//form[@id='customerSignInForm']"):
#             return self.login(response)
#         else:
#             return self.get_section_links(response)
#
#     def login(self, response):
#         self.log("Login page... Posting username & password")
#         self.log(f"!!!!!!!!!!!!!login, {type(response)}")
#         # formdata = {'Username': 'admin', 'Password': 'password'}
#         # formdata = {"username": "osl@famaga.de", "password": "FamagaKitov777!"}
#         formdata = {"email": "osl@famaga.de", "password": "FamagaKitov777!"}
#         return FormRequest.from_response(
#             response, formdata=formdata, callback=self.parse, dont_filter=True)
#
#     def get_section_links(self, response):
#         self.log("Logged in... Grabbing links...")
#         self.log(f"!!!!!!!!!!!!!get_section_links, {type(response)}")
#         yield scrapy.Request(
#                         "https://www.camlogic.it/en/products/detail/pfg05at-atf_241?code=PFG055-FC3NN020004-1CP0TF#productDetailConfiguratorAnchor",
#                         callback=self.parse_2
#                     )
#
#         # for section in hxs.select("//select[@id='SubsitesSelect']//option"):
#         #     value = section.select("@value").extract()[0]
#         #     text = section.select("text()").extract()[0]
#         #     yield MyItem(value=value, text=text)
#     def parse_2(self, response):
#         result = dict()
#         result["url"] = response.url
#         result["Цена"] = response.css("div.card-body span.discounted_price")
#         self.log(f"!!!!!!!!!!!!! parse_2, {type(response)}")
#
#         yield result
#
#     async def errback(self, failure):
#         save_error(failure.request.url, failure, "ERRBACK", err_file_path=ERRORS_DIR / "errback.csv")
#
# # from bihl_wiedemann_de.spiders.bihl_wiedemann_spyder import *
