import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get("https://www.balluff.com/de-de/products/BCC032H?pf=G1102&pm=S-BCC%20SE%20SCU")
browser.maximize_window()
try:
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Allem zustimmen')]"))
    )
    button = browser.find_element(By.XPATH, "//*[contains(text(), 'Allem zustimmen')]")
    browser.execute_script("arguments[0].click();", button)
    print('Приняли куки')
    time.sleep(3)
except Exception as e:
    print(f"Ошибка клика по кнопке: {e}")

try:
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="top-price"]/div/div/div[2]/button'))
    )
    button = browser.find_element(By.XPATH, '//*[@id="top-price"]/div/div/div[2]/button')
    browser.execute_script("arguments[0].click();", button)
    time.sleep(3)
except Exception as e:
    print(f"Ошибка клика по кнопке 'Daten abfragen': {e}")


browser.quit()
