from selenium import webdriver

from ..config import settings


class BrowserFactory:
    def __init__(self, browser_name):
        self.browser_name = browser_name

    def get_webdriver_instance(self):
        if self.browser_name == "chrome":
            options = webdriver.ChromeOptions()
            for opt in settings["chrome_options"].to_list():
                options.add_argument(opt)
            driver = webdriver.Chrome(options=options)

        elif self.browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            # for opt in settings["firefox_options"].to_list():
            #     options.add_argument(opt)
            driver = webdriver.Firefox(options=options)

        driver.maximize_window()

        return driver
