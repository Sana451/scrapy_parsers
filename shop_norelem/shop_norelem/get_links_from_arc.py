import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

with open(
        "/home/sana451/PycharmProjects/scrapy_norelem/parsers/shop_norelem/shop_norelem/арт-лы norelem - артикулы.csv") as csvfile:
    reader = csv.reader(csvfile)
    articles = list(reader)[1:]
    articles = [art[0] for art in articles if art[0]]

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
browser = webdriver.Chrome(options=options)

with open(
        "/home/sana451/PycharmProjects/scrapy_norelem/parsers/shop_norelem/shop_norelem/add_links.csv",
        "w") as csvfile:
    writer = csv.writer(csvfile)

    for art in articles:
        browser.get("https://norelem.de/en/")
        input_fld = browser.find_elements(
            By.XPATH, "//input[@placeholder='Search for category, product name, item number...']")[0]
        input_fld.send_keys(art)
        input_fld.send_keys(Keys.ENTER)
        writer.writerow(browser.current_url)

browser.close()
