from selenium.webdriver.common.by import By

from .base_element import BaseElement
from ..logger import MyLogger


class RegistrationForm(BaseElement):
    log = MyLogger.__call__().get_logger()

    def __init__(self):
        super().__init__(locator=(By.XPATH, "//*[contains(text(), 'Registration F')]"), name="RegForm")

    __TITLE = (By.XPATH, "//*[@id='registration-form-modal']")
    __FIRST_NAME_FIELD = (By.XPATH, "//*[@id='firstName']")
    __LAST_NAME_FIELD = (By.XPATH, "//*[@id='lastName']")
    __EMAIL_FIELD = (By.XPATH, "//*[@id='userEmail']")
    __AGE_FIELD = (By.XPATH, "//*[@id='age']")
    __SALARY_FIELD = (By.XPATH, "//*[@id='salary']")
    __DEPARTMENT_FIELD = (By.XPATH, "//*[@id='department']")
    __SUBMIT_BTN = (By.XPATH, "//*[@id='submit']")

    def type_first_name(self, first_name):
        self.send_keys_to_element(self.__FIRST_NAME_FIELD, first_name)

    def type_last_name(self, last_name):
        self.send_keys_to_element(self.__LAST_NAME_FIELD, last_name)

    def type_email(self, email):
        self.send_keys_to_element(self.__EMAIL_FIELD, email)

    def type_age(self, age):
        self.send_keys_to_element(self.__AGE_FIELD, age)

    def type_salary(self, salary):
        self.send_keys_to_element(self.__SALARY_FIELD, salary)

    def type_department(self, department):
        self.send_keys_to_element(self.__DEPARTMENT_FIELD, department)

    def click_submit_btn(self):
        self.element_click(self.__SUBMIT_BTN)

    def register_user(self, user):
        self.type_first_name(user["first_name"])
        self.type_last_name(user["last_name"])
        self.type_email(user["email"])
        self.type_age(user["age"])
        self.type_salary(user["salary"])
        self.type_department(user["department"])
        self.log.info(f"{self.name} введены данные {user.values()}")
        self.click_submit_btn()
        self.log.info(f"{self.name} форма отправлена")

    def check_user_registered(self, user):
        __FIRST_NAME_TD = (By.XPATH, f"//*[@class='rt-td' and contains(text(), '{user['first_name']}')]")
        __LAST_NAME_TD = (By.XPATH, f"//*[@class='rt-td' and contains(text(), '{user['last_name']}')]")
        __AGE_TD = (By.XPATH, f"//*[@class='rt-td' and contains(text(), '{user['age']}')]")
        __EMAIL_TD = (By.XPATH, f"//*[@class='rt-td' and contains(text(), '{user['email']}')]")
        __SALARY_TD = (By.XPATH, f"//*[@class='rt-td' and contains(text(), '{user['salary']}')]")
        __DEPARTMENT_TD = (By.XPATH, f"//*[@class='rt-td' and contains(text(), '{user['department']}')]")

        if (
                self.element_is_displayed(__FIRST_NAME_TD) and
                self.element_is_displayed(__LAST_NAME_TD) and
                self.element_is_displayed(__AGE_TD) and
                self.element_is_displayed(__EMAIL_TD) and
                self.element_is_displayed(__SALARY_TD) and
                self.element_is_displayed(__DEPARTMENT_TD)
        ):
            self.log.debug(f"{self.name} успех регистрации {user.values()}")
            return True
        else:
            self.log.debug(f"{self.name} неудачная регистрация {user.values()}")
            return False
