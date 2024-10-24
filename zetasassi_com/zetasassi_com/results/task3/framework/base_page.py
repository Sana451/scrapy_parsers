from selenium.common import ElementClickInterceptedException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..config import settings
from .browser import Driver
from .logger import MyLogger


class BasePage:
    log = MyLogger.__call__().get_logger()

    def __init__(self, locator, name):
        self.locator = locator
        self.name = name

    def open_page(self, url):
        Driver().get_driver().get(url)
        self.log.debug(f"{self.name} открыта")

    def page_opened(self):
        is_opened = self.find_element(self.locator).is_displayed()
        if is_opened:
            self.log.info(f"{self.name} открыта")
        else:
            self.log.info(f"{self.name} не открыта")
        return is_opened

    def find_element(self, locator):
        try:
            return WebDriverWait(Driver().get_driver(), settings["default_timeout"]).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException as exc:
            self.log.error(f"{self.name} find_element with {locator} method returned TimeoutException")
            raise TimeoutException

    def find_elements(self, locator):
        try:
            return WebDriverWait(Driver().get_driver(), settings["default_timeout"]).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException as exc:
            self.log.error(f"{self.name} find_elements with {locator} method returned TimeoutException")
            raise TimeoutException

    def get_elements_count(self, locator):
        count = len(self.find_elements(locator))
        self.log.debug(f"{self.name} get_elements_count with {locator} returned {count}")
        return count

    def get_element_text(self, locator):
        text = self.find_element(locator).text
        self.log.debug(f"{self.name} get_element_text with {locator} returned {text}")
        return text

    def find_clickable(self, locator):
        try:
            return WebDriverWait(Driver().get_driver(), settings["default_timeout"]).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException as exc:
            self.log.error(f"{self.name} find_clickable with {locator} method returned TimeoutException")
            raise TimeoutException

    def element_click(self, locator):
        try:
            try:
                self.find_clickable(locator).click()
                self.log.debug(f"{self.name} clicked element {locator}")
            except (ElementNotInteractableException, ElementClickInterceptedException) as exc:
                Driver().get_driver().execute_script("arguments[0].click();", self.find_clickable(locator))
                self.log.debug(f"{self.name} clicked element {locator}")

        except Exception as exc:
            self.log.error(f"{self.name} element_click with {locator} method returned exception")
            raise exc

    def switch_to_new_tab(self):
        Driver().switch_to_new_tab()
        self.log.debug(f"{self.name} switched to new tab")

    def get_alert_text(self):
        text = Driver().get_alert_text()
        self.log.debug(f"{self.name} get_alert_text retrived text: {text}")
        return text

    def accept_alert(self):
        Driver().accept_alert()
        self.log.debug(f"{self.name} accepted alert")

    def check_alert_closed(self):
        is_closed = not Driver().check_alert_is_displayed()
        self.log.debug(f"{self.name} check_alert_closed method return {is_closed}")
        return is_closed

    def send_keys_to_prompt_box(self, text):
        Driver().type_to_prompt(text)
        self.log.debug(f"{self.name} sent {text} to prompt")

    def switch_to_frame(self, locator):
        frame = self.find_element(locator)
        Driver().switch_to_iframe(frame)
        self.log.debug(f"{self.name} switched to frame")

    def switch_to_default_content(self):
        Driver().switch_to_default_content()
        self.log.debug(f"{self.name} switched to default content")

    def tabs_count(self):
        count = Driver().tabs_count()
        self.log.info(f"{self.name} counted {count} opened tabs")
        return count

    def close_current_tab(self):
        Driver().close_current_tab()
        self.log.info(f"{self.name} закрыл текущую вкладку")

    def switch_to_default_tab(self):
        Driver().switch_to_default_tab()
        self.log.info(f"{self.name} переключился на основную вкладку")
