import csv
import json
import sys
import time
from typing import Iterable

import pandas
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC

import requests
from selenium import webdriver
from scrapy import Request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from tabulate import tabulate

with open("/home/sana451/PycharmProjects/scrapy_parsers/balluff_com/balluff_com/results/balluff.com.articles.csv",
          "r") as f:
    reader = csv.reader(f)
    articles = [row[0] for row in list(reader)[1:]]

browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://www.balluff.com/de-de")
try:
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Allem zustimmen')]"))
    )
    button = browser.find_element(By.XPATH, "//*[contains(text(), 'Allem zustimmen')]")
    browser.execute_script("arguments[0].click();", button)
    print('Приняли куки')
    time.sleep(3)
except Exception as e:
    print(f"Ошибка клика по кнопке: {e}")

browser.find_element(By.XPATH, "//button[@x-show='!searchOpen']").click()

all_links = set()

for art in articles[553:]:
    browser.find_elements(By.XPATH, "//input[@type='text']")[0].clear()
    time.sleep(2)
    browser.find_elements(By.XPATH, "//input[@type='text']")[0].send_keys(art)
    time.sleep(2)
    browser.find_elements(By.XPATH, "//input[@type='text']")[0].send_keys(Keys.ENTER)
    time.sleep(2)
    try:
        links_elements = WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//div[@class='mb-4']//a[contains(@class, 'hover:text-accent')]",
                )
            )
        )

        links = [a.get_attribute("href") for a in links_elements]
        all_links.update(links)
        with open("/home/sana451/PycharmProjects/scrapy_parsers/balluff_com/balluff_com/results/balluff.com.links3.csv",
                  "a") as f:
            writer = csv.writer(f)
            for i in links:
                writer.writerow([i])

    except Exception as error:
        print(art, "Not found links")
        with open(
                "/home/sana451/PycharmProjects/scrapy_parsers/balluff_com/balluff_com/results/balluff.com.not_founded_articles.csv",
                "a") as f:
            writer = csv.writer(f)
            writer.writerow([art, error])

browser.quit()

pandas.DataFrame(all_links).to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/balluff_com/balluff_com/results/balluff.com.links2.csv", index=False)
