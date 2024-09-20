import csv
import itertools
import re
import time
from pathlib import Path

from seleniumwire import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import scrapy
from scrapy.shell import inspect_response
from tabulate import tabulate


options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")

seleniumwire_options = {
    'proxy': {
        'http': 'http://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
        'https': 'https://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

browser = webdriver.Chrome(seleniumwire_options=seleniumwire_options, options=options)


try:
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
    )
    accept_cookie_btn = browser.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    accept_cookie_btn.click()
except Exception:
    pass

try:
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, "customerSignInForm"))
    )
    form = browser.find_element(By.ID, "customerSignInForm")
    form.find_element(By.CSS_SELECTOR, "input[type=email]").send_keys("osl@famaga.de")
    form.find_element(By.CSS_SELECTOR, "input[type=password]").send_keys("FamagaKitov777!")
    form.find_element(By.ID, "front-remember-me-cb").click()
    browser.find_element(By.CSS_SELECTOR, "button.loginSubmitBtn").click()
except Exception:
    pass

WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-header"))
)

with open("/home/sana451/PycharmProjects/scrapy_parsers/camlogic_it/camlogic_it/results/Product_export_20240918121434.csv", encoding='utf-16') as csv_file:
    reader = csv.reader(csv_file, delimiter=";")
    articles = list(reader)[1:]
    new_articles = [[a[-1], a[-2]] for a in articles]
    articles = list(itertools.chain(*articles))
    new_articles = [i for i in articles if (i != 'CAMLogic' and i != '' and not i.isdigit())]


for art in new_articles:
    browser.get("https://www.camlogic.it/en/level-sensors?search={art}")
    suop = BeautifulSoup(browser.page_source)
    links = suop.select("div.product-wrapper a")