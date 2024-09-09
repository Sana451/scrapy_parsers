# import csv
# import time
# from pathlib import Path
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# import scrapy
# from scrapy.shell import inspect_response
# from selenium.webdriver.common.by import By
#
# # div.product - category - lister
# DOMAIN = "https://www.norgren.com"
# CURRENT_DIR = Path("__file__").resolve()
# BASE_DIR = CURRENT_DIR.parent.parent
# RESULTS_DIR = BASE_DIR / "results"
# LINKS_DIR = BASE_DIR / "links"
# ERRORS_DIR = BASE_DIR / "errors"
# ERRORS_FILENAME = ERRORS_DIR / "errors.csv"
#
# print(BASE_DIR)
# print(RESULTS_DIR)
#
# with open(RESULTS_DIR / "cactegories_links.csv") as cat_links_file:
#     reader = csv.reader(cat_links_file)
#     start_urls = list(reader)[1:]
#
# browser = webdriver.Chrome()
# for url in start_urls:
#     print(url)
#     print(url[0])
#     browser.get(url[0])
#
# browser.quit()
