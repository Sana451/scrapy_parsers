import csv

import pandas
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#
# with open(
#         "/home/sana451/PycharmProjects/scrapy_parsers/norgren_com/norgren_com/results/cactegories_links.csv") as cat_file:
#     reader = csv.reader(cat_file)
#     cat_links = list(reader)[17:]
#
# result = []
#
# file = open("/home/sana451/PycharmProjects/scrapy_parsers/norgren_com/norgren_com/results/product_links_v2.csv", "a")
# writer = csv.writer(file)
#
# for cat in cat_links:
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless=new")
#     options.add_argument('--disable-blink-features=AutomationControlled')
#     browser = webdriver.Chrome(options=options)
#
#     i = 1
#     next_page = True
#     while next_page is True:
#         page_link = cat[0] + f'?page={i}'
#         print(page_link)
#         browser.get(page_link)
#         try:
#             WebDriverWait(browser, 10).until(
#                 EC.element_to_be_clickable((By.ID, "ensAcceptAll"))
#             ).click()
#         except TimeoutException:
#             pass
#
#         try:
#             WebDriverWait(browser, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "body h4 a"))
#             )
#         except TimeoutException:
#             browser.refresh()
#             WebDriverWait(browser, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "body h4 a"))
#             )
#         finally:
#             urls = browser.find_elements(By.CSS_SELECTOR, "body h4 a")
#             hrefs = [a.get_attribute('href') for a in urls]
#             result.extend(hrefs)
#
#             for h in hrefs:
#                 writer.writerow([h])
#                 file.flush()
#
#             i += 1
#
#         try:
#             WebDriverWait(browser, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "link[rel='next']"))
#             )
#         except TimeoutException:
#             next_page = False
#         finally:
#             print(len(result))
#
# browser.quit()
# file.close()
# # pandas.DataFrame(result).to_csv(
# #     "/home/sana451/PycharmProjects/scrapy_parsers/norgren_com/norgren_com/results/product_links_v2.csv", index=False)
DOMAIN = "https://www.landefeld.com"

response = requests.get(r"https://www.landefeld.com/katalog/en/imi-norgren/%7B84C19EB7-3427-4EE9-8941-D70340F2DF7C%7D")
soup = BeautifulSoup(response.content)
categories = soup.select("a.item-link")
cat_links = [f"{DOMAIN}{a['href']}" for a in categories]
print(len(cat_links), cat_links)
#
# pandas.DataFrame(cat_links).to_csv(
#     "/home/sana451/PycharmProjects/scrapy_parsers/landefeld_com/landefeld_com/results/categories.csv", index=False)
# result = []
#
#
# for cat in cat_links:
#     options = webdriver.ChromeOptions()
#     # options.add_argument("--headless=new")
#     options.add_argument('--disable-blink-features=AutomationControlled')
#     browser = webdriver.Chrome(options=options)
#   re
#     i = 1
#     next_page = True
#     while next_page is True:
#         browser.get(cat)
#         try:
#             WebDriverWait(browser, 10).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mehranzeigen button"))
#             ).click()
#         except TimeoutException:
#             next_page = False
#             product_links = browser.find_elements(By.CSS_SELECTOR, "div.artikelliste-artikelgruppe div.row a")
#             result.extend([f"{DOMAIN}{a['href']}" for a in product_links])
#             print(product_links)
#             print(len(product_links))
#         finally:
#             browser.quit()
