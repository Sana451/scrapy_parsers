from selenium.common import NoAlertPresentException

from .singleton import Singleton
from .browser_factory import BrowserFactory
from .logger import MyLogger


class Driver(metaclass=Singleton):
    log = MyLogger.__call__().get_logger()

    def __init__(self, browser_name):
        self.__driver = None
        self.browser_name = browser_name

    def get_driver(self):
        if self.__driver is None:
            bf = BrowserFactory(self.browser_name)
            self.__driver = bf.get_webdriver_instance()
            return self.__driver
        return self.__driver

    def del_driver(self):
        if self.__driver is not None:
            self.get_driver().quit()
            self.__driver = None

    def check_alert_is_displayed(self):
        try:
            self.__driver.switch_to.alert
            self.log.debug("Driver переключился на alert")
            return True
        except NoAlertPresentException:
            self.log.debug("Driver не переключился на alert т.к. alert не найден")
            return False

    def switch_to_alert(self):
        if self.check_alert_is_displayed() is True:
            self.log.debug("Driver: переключился на alert")
            return self.__driver.switch_to.alert

    def get_alert_text(self):
        if self.check_alert_is_displayed() is True:
            text = self.switch_to_alert().text
            self.log.debug(f"Driver: извлёк {text} из alert")
            return text

    def accept_alert(self):
        self.log.info("Driver: подтвердил alert")
        return self.switch_to_alert().accept()

    def type_to_prompt(self, text):
        if self.check_alert_is_displayed() is True:
            self.switch_to_alert().send_keys(text)
            self.log.info(f"Driver: вввёл текст: {text} в prompt")

    def switch_to_iframe(self, frame):
        self.__driver.switch_to.frame(frame)
        self.log.debug(f"Driver: переключился на frame")

    def switch_to_default_content(self):
        self.__driver.switch_to.default_content()
        self.log.debug(f"Driver: переключился на основной контент")

    def switch_to_new_tab(self):
        windows = self.__driver.window_handles
        self.__driver.switch_to.window(windows[-1])
        self.log.debug(f"Driver: переключился на новую вкладку")

    def close_current_tab(self):
        self.__driver.close()
        windows = self.__driver.window_handles
        self.__driver.switch_to.window(windows[-1])
        self.log.debug(f"Driver: закрыл текущую вкладку")

    def switch_to_default_tab(self):
        windows = self.__driver.window_handles
        self.__driver.switch_to.window(windows[0])
        self.log.debug(f"Driver: переключился на основной контент")

    def tabs_count(self):
        self.log.debug(f"Driver: на данный момент открыто {len(self.__driver.window_handles)} вкладок")
        return len(self.__driver.window_handles)
