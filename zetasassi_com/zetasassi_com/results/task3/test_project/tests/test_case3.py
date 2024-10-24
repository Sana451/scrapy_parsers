import pytest

from ...config import settings
from ..pages.main_page import MainPage
from ...framework.logger import MyLogger

log = MyLogger.__call__().get_logger()


@pytest.mark.parametrize("user", [(settings["user_1"]), (settings["user_2"])])
class TestCase3Tables:
    def test_case_3_tables(self, user):
        log.info("Testcase 3. Tables")
        log.info("Шаг 1. Перейти на главную страницу")
        m_p = MainPage()
        m_p.open_page(settings["main_page_url"])
        assert m_p.page_opened(), "Страница не открыта"

        log.info("Шаг 2. Кликнуть на кнопку 'Elements', кликнуть пункт 'Web Tables'")
        m_p.click_elements_btn()
        m_p.click_web_tables_btn()
        assert m_p.web_tables_form_on_page(), "Страница с формой 'Web Tables' не открыта"

        log.info("Шаг 3. Кликнуть на кнопку 'Add'")
        m_p.click_add_report_btn()
        assert m_p.registration_form_on_page(), "На странице не появилась форма 'Registration Form'"

        log.info(f"Шаг 4. Ввести данные пользователя {user.values()}, и нажать на кнопку Submit")
        m_p.reg_form.register_user(user)
        assert m_p.reg_form.check_user_registered(user) is True, "В таблице не появились данные user1"

        log.info(f"Шаг 5.  Нажать на кнопку 'Delete' в строке пользователя {user.values()}")
        registered_users_before_del = m_p.registered_users_count()
        m_p.click_delete_last_register_user_btn()
        assert registered_users_before_del > m_p.registered_users_count(), "Кол-во записей в таблице не изменилось"
        assert m_p.reg_form.check_user_registered(user) is False, "Пользователь не удалился из таблицы"
