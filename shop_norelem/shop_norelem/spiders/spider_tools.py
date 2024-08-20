from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


HOSTNAME = "https://norelem.de"


def click_cookie_bot(browser, url):
    browser.get(url)

    button = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
            )
        )
    )
    if isinstance(button, WebElement):
        button.click()
    else:
        click_cookie_bot(browser, url)


def find_table_tool(browser):
    try:
        table = browser.find_element(By.CSS_SELECTOR, "div.product-table a[data-id]")
        if isinstance(table, WebElement):
            return table
    except NoSuchElementException:
        return None


def find_element_tool(browser, by_variant, selector: str):
    try:
        element = browser.find_element(by_variant, selector)
        if isinstance(element, WebElement):
            return element
    except NoSuchElementException:
        return None
