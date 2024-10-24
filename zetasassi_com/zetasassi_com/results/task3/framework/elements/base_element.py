from selenium.common import TimeoutException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ...config import settings
from ..browser import Driver
from ..logger import MyLogger


class BaseElement:
    log = MyLogger.__call__().get_logger()

    def __init__(self, locator, name):
        self.locator = locator
        self.name = name

    def find_element(self, locator):
        try:
            return WebDriverWait(Driver().get_driver(), settings["default_timeout"]).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException as exc:
            self.log.debug(f"{self.name} not found {locator} because TimeoutException")
            return None

    def element_is_displayed(self, locator):
        element = self.find_element(locator)
        if element:
            if element.is_displayed():
                self.log.debug(f"{self.name} element_is_displayed {locator} returned True")
                return True
            else:
                self.log.debug(f"{self.name} element_is_displayed {locator} returned False")
                return False

    def element_click(self, locator):
        try:
            self.find_clickable(locator).click()
            self.log.debug(f"{self.name} clicked element {locator}")
        except (ElementNotInteractableException, ElementClickInterceptedException) as exc:
            Driver().get_driver().execute_script("arguments[0].click();", self.find_clickable(locator))
            self.log.debug(f"{self.name} clicked element {locator}")

    def find_clickable(self, locator):
        return WebDriverWait(Driver().get_driver(), settings["default_timeout"]).until(
            EC.element_to_be_clickable(locator)
        )

    def send_keys_to_element(self, locator, text):
        self.find_element(locator).send_keys(text)
        self.log.debug(f"{self.name} typed text: {text} to element {locator}")
