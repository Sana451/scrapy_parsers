# import csv
# import json
# import sys
#
# import requests
# from tabulate import tabulate
#
# sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
# from tools import my_scraping_tools as my_tools  # from bs4 import BeautifulSoup
#
# from pathlib import Path
#
# import scrapy
# from urllib.parse import urlencode, quote_plus
#
# BASE_DIR = Path("__file__").resolve().parent
# RESULTS_DIR = BASE_DIR / "results"
# ERRORS_DIR = BASE_DIR / "errors"
# ERRORS_FILENAME = ERRORS_DIR / "errors.csv"
#
#
# def ZenRows_api_url(url, api_key):
#     # set ZenRows request parameters
#     params = {
#         "apikey": api_key,
#         "url": url,
#         "js_render": "true",
#         "premium_proxy": "true",
#     }
#     # encode the parameters and merge it with the ZenRows base URL
#     encoded_params = urlencode(params, quote_via=quote_plus)
#
#     final_url = f"https://api.zenrows.com/v1/?{encoded_params}"
#
#     return final_url
#
#
# class AirComPlSpiderSpider(scrapy.Spider):
#     name = "air_com_pl_spider"
#     allowed_domains = ["air-com.pl", "zenrows.com"]
#
#     def start_requests(self):
#         with open(RESULTS_DIR / "air-com.pl.camozzi.links.csv", "r", encoding="utf-8") as links_file:
#             reader = csv.reader(links_file)
#             start_urls = [url[0] for url in list(reader)]
#             for url in start_urls[:10]:
#                 api_url = ZenRows_api_url(url, "99ee1ed06dee541b7bdbb5b645227e9dfcc52262")
#                 yield scrapy.Request(
#                     url=api_url,
#                     callback=self.parse,
#                     cb_kwargs={"resp_url": url}
#                 )
#
#     def parse(self, response, resp_url):
#         # f = open("1.html", "w")
#         # f.write(response.text)
#         # f.close()
#         result = dict()
#         result["url"] = resp_url
#
#         try:
#             field = "Артикул"
#             result[field] = response.css("h2.product-signs-info span::text").get().strip()
#         except Exception as error:
#             result[field] = ""
#             my_tools.save_error(response.url, error, field, ERRORS_FILENAME)
#
#         yield result
