import csv
import re
import time
from pathlib import Path

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import scrapy
from scrapy.shell import inspect_response
from seleniumwire import webdriver
from tabulate import tabulate

DOMAIN = "https://www.camlogic.it"

BASE_DIR = Path("__file__").resolve().parent

RESULTS_DIR = BASE_DIR / "results"
ERRORS_DIR = BASE_DIR / "errors"
ERRORS_FILENAME = ERRORS_DIR / "errors.csv"

articles = ['RIC-YY01-PFG051-GEXXX0200YY--YY0002',
            'RIC-CP-PFG051-FA1CP0400XX-',
            'RIC-CP-PFG861-FA1CP0400XX-',
            'RIC-SP-PFG051-FA1SP030003-',
            'RIC-SP-PFG861-FA1SP020003-',
            'RIC-CX-PFG051-FA1CX040003-',
            'RIC-CX-PFG861-FA1CX040003-',
            'RIC-SX-PFG051-FA1SX030003-',
            'RIC-SX-PFG861-FA1SX030003-',
            'RIC-PF-PFG051-XXXPF0500XX-',
            'RIC-PF-PFG861-XXXPF0500XX-',
            'RIC-RB-PFG051-GH1RB060006--RB0043',
            'RIC-RB-PFG861-GH1RB060006--RB0043',
            'RIC-RA-PFG051-FA1RA060003-',
            'RIC-RC-PFG051-GH1RC060003--RC0013',
            'RIC-RC-PFG861-GH1RC060003--RC0013',
            'RIC-RD-PFG051-GH1RD050006-',
            'RIC-RD-PFG861-GH1RD050006--RD0013',
            'RIC-PFR-PFG051-XXXPR0500XX-',
            'RIC-CC05-PFG056-GE1XXXXXXXX-TF',
            'RIC-CC05-PFG051-GE1XXXXXXXX-TF',
            'RIC-CC05-PFG052-GE1XXXXXXXX-',
            'RIC-CC05-PFG053-GE1XXXXXXXX-',
            'RIC-CC05-PFG055-GE1XXXXXXXX-',
            'RIC-CS05-PFG051-GE1XXXXXXXX-TF',
            'RIC-CS05-PFG052-GE1XXXXXXXX-',
            'RIC-CS05-PFG053-GE1XXXXXXXX-',
            'RIC-CS05-PFG055-GE1XXXXXXXX-',
            'RIC-CS05-PFG056-GE1XXXXXXXX-',
            'RIC-MT05-PFG056-GE1XXXXXXXX-',
            'RIC-MT05-PFG051-GE1XXXXXXXX-',
            'RIC-MT05-PFG052-GE1XXXXXXXX-',
            'RIC-MT05-PFG053-GE1XXXXXXXX-',
            'RIC-MT05-PFG055-GE1XXXXXXXX-',
            'RIC-CF-PFG053-FB1CF040004-',
            'RIC-SX05XF-PFG053-FB1SX030004-',
            'RIC-RC05XF-PFG053-FB1RC060003-',
            'RIC-RD05XF-PFG053-FB1RD050004-',
            'RIC-PF05X-PFG053-GH1PF050005-',
            'RIC-SX05X-PFG053-GH1SX030005-',
            'RIC-CX05X-PFG863-GH1CX040006-',
            'RIC-CX05X-PFG053-GH1CX040006-',
            'RIC-RC05X-PFG053-GH1RC060005-',
            'RIC-RD05X-PFG053-GH1RD050005-',
            'RIC-PA-PFG055-GH1PF050004-',
            'RIC-MT86-PFG861-GE1XXXXXXXX-',
            'RIC-MT86-PFG863-GE1XXXXXXXX-',
            'RIC-MT86-PFG865-GE1XXXXXXXX-',
            'RIC-MT86-PFG866-GE1XXXXXXXX-',
            'RIC-CC86-PFG866-GE1XXXXXXXX-',
            'RIC-CP57-PFG091-GF1CP030002-',
            'RIC-CP57-PFG571-GF1CP030002-',
            'RIC-SP57-PFG091-GF1SP010002-',
            'RIC-SP57-PFG571-GF1SP020002-',
            'RIC-CX57-PFG091-GF1CX030001-',
            'RIC-CX57-PFG571-GF1CX030001-',
            'RIC-CX57-PFG573-GF1CX030001-',
            'RIC-SX57-PFG091-GF1SX030001-',
            'RIC-SX57-PFG571-GF1SX020001-',
            'RIC-SX57-PFG573-GF1SX030001-',
            'RIC-RB57-PFG091-GF1RB060002-',
            'RIC-RB57-PFG571-GF1RB060002-',
            'RIC-RB57-PFG573-GF1RB57010001-',
            'RIC-RA57-PFG571-GF1RA050002-',
            'RIC-RA57-PFG573-GF1RA57010002-',
            'RIC-RC57-PFG091-GF1RC050002-',
            'RIC-RC57-PFG571-GF1RC050002-',
            'RIC-RC57-PFG573-GF1RC050002-',
            'RIC-RD57-PFG091-XXXRD0600XX-',
            'RIC-RD57-PFG573-XXXRD0600XX--RD0005',
            'RIC-PF57-PFG091-XXXPF1000XX-',
            'RIC-PF57-PFG571-XXXPF1000XX-',
            'RIC-PF57-PFG573-XXXPR0500XX-',
            'RIC-PF0-PFG571-XXXPR1000XX-',
            'RIC-CC57-PFG571-GD1XX0100XX-TF',
            'RIC-CC57-PFG093-GD1XX0100XX-TF',
            'RIC-CC57-PFG573-GD1XX0100XX-TF',
            'RIC-CC57-PFG575-GD1XX0100XX-TF',
            'RIC-CC57-PFG577-GD4XX0100XX-',
            'RIC-CC57-PFG091-GD1XX0100XX-TF',
            'RIC-CC57-PFG092-GD1XX0100XX-TF',
            'RIC-CS57-PFG093-GD1XX0100XX-TF',
            'RIC-CS57-PFG092-GD1XX0100XX-TF',
            'RIC-CS57-PFG091-GD1XX0100XX-TF',
            'RIC-CS57-PFG571-GD1XX0100XX-TF',
            'RIC-CS57-PFG573-GD1XX0100XX-TF',
            'RIC-CS57-PFG575-GD1XX0100XX-TF',
            'RIC-MT57-PFG091-GD1XX0100XX-',
            'RIC-MT57-PFG571-GD1XX0100XX-',
            'RIC-MT57-PFG577-GDXXX0100XX-',
            'RIC-GC-PFGLP2-FBNN0000-GC',
            'RIC-GC-PFGLP1-GGNN250-GC',
            'RIC-GD-PFGLP2-FBNN0000-GD',
            'RIC-GD-PFGLP1-GGNN250-GD']


def del_classes_AND_divs_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    [d.decompose() for d in soup.find_all("div")]

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def del_classes_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name", "href", "title"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(["class", "style", "id", "scope", "data-th", "target"]):
        data.decompose()

    return ' '.join(soup.stripped_strings)


def create_html_table(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    res = []
    divs = soup.find_all("div")
    for div in divs:
        span_list = div.find_all("span")
        if len(span_list) == 2:
            res.append(i.text.strip() for i in span_list)

    html = tabulate(res, tablefmt="html").replace("\n", "")

    return html


def save_error(url, error, field, err_file_path=ERRORS_FILENAME):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


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
# browser.implicitly_wait(20)
browser.get("https://www.camlogic.it/en/login?redir=%2Fen%2Fuser")

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


def scrapy_page(browser, url):
    time.sleep(5)
    browser.get(url)

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.prod-code"))
    )

    result = dict()
    result["url"] = url.rstrip("#productDetailConfiguratorAnchor")

    try:
        field = "Заголовок"
        result[field] = browser.find_element(By.CSS_SELECTOR, "h1.prod-code").text
    except Exception as error:
        result[field] = ""
        save_error(url, error, field)

    try:
        field = "Commercial code"
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".sellCode"))
        )
        result[field] = browser.find_element(By.CSS_SELECTOR, ".sellCode").text
    except Exception as error:
        result[field] = ""
        save_error(url, error, field)

    try:
        field = "Configuration code"
        result[field] = browser.find_element(By.CSS_SELECTOR, ".configurationCode").text
    except Exception as error:
        result[field] = ""
        save_error(url, error, field)

    try:
        field = "Цена"
        result[field] = browser.find_element(By.CSS_SELECTOR, "div.card-body span.full_price"
                                             ).text.replace("€", "")
    except Exception as error:
        try:
            result[field] = browser.find_element(By.CSS_SELECTOR, "div.price-label strong"
                                                 ).text.replace("€", "")
        except Exception:
            result[field] = ""
        save_error(url, error, field)

    try:
        field = "Цена со скидкой"
        result[field] = browser.find_element(By.CSS_SELECTOR, "div.card-body span.discounted_price"
                                             ).text.replace("€", "")
    except Exception as error:
        try:
            result[field] = browser.find_element(By.CSS_SELECTOR, "div.out-of-prod span").text
        except Exception:
            result[field] = ""
        save_error(url, error, field)

    try:
        field = "Скидка"
        result[field] = browser.find_element(By.CSS_SELECTOR, "#productDetailConfigurator span.discount_label"
                                             ).text.replace("Discount", "")
    except Exception as error:
        result[field] = ""
        save_error(url, error, field)

    try:
        field = "Картинки"
        images = browser.find_elements(By.CSS_SELECTOR, "img.img-web-ext")
        images_src = [img.get_attribute("src") for img in images if "placeholder" not in img.get_attribute("src")]
        result[field] = " | ".join(images_src)
    except Exception as error:
        result[field] = ""
        save_error(url, error, field)

    try:
        field = "PDF"
        div = browser.find_element(By.CSS_SELECTOR, "div#collapse_tech")
        pdf = div.find_element(By.XPATH, "//a[contains(text(), 'Technical datasheet')]")
        result[field] = pdf.get_attribute("href")
    except Exception as error:
        result[field] = ""
        save_error(url, error, field)

    try:
        field = "Описание"
        description = browser.find_element(By.CSS_SELECTOR, "div.prod-desc p").text
        result[field] = description
    except Exception as error:
        result[field] = ""
        save_error(url, error, field)

    try:
        field = "Technical Specifications"
        details = browser.find_element(
            By.CSS_SELECTOR, "div.productDetailAdvantages div.info-wrapper ul").get_attribute("outerHTML")

        result[field] = details
    except Exception as error:
        result[field] = ""
        save_error(url, error, field)

    try:
        field = "Specifications"
        specs = browser.find_elements(By.CSS_SELECTOR, "div.prod-desc ul")
        all_specs = [del_classes_from_html(spec.get_attribute("outerHTML")) for spec in specs]
        result[field] = "\n".join(all_specs)
    except Exception as error:
        result[field] = ""
        save_error(url, error, field)

    try:
        field = "Категории"
        product_line = browser.find_element(By.XPATH, "//p[contains(text(), 'Product line')]")
        category = product_line.find_element(By.TAG_NAME, "a").text
        result[field] = category
    except Exception as error:
        result[field] = ""
        save_error(url, error, field)

    # browser.quit()
    return result


with open(RESULTS_DIR / "links.csv") as cat_links_file:
    reader = csv.reader(cat_links_file)
    start_urls = list(reader)

with open(RESULTS_DIR / "camlogic.it.v3.csv", "w") as sel_res_file:
    writer = csv.DictWriter(sel_res_file, fieldnames=[
        "url", "Заголовок", "Commercial code", "Configuration code", "Цена", "Цена со скидкой",
        "Скидка", "Картинки", "PDF", "Описание", "Technical Specifications", "Specifications", "Категории"])
    writer.writeheader()

    for article in articles:
    # for url in start_urls:
        res = scrapy_page(browser, f"https://www.camlogic.it/en/level-sensors?search={article}")
        # res = scrapy_page(browser, url[0])
        writer.writerow(res)

# PROXY = "vk0dUcb:Us5jxS8o88@23.27.3.254:59100"
