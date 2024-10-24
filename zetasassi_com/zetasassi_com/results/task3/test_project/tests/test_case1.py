from ...config import settings
from ..pages.main_page import MainPage
from ...framework.test_tools.test_tools import gen_random_string
from ...framework.logger import MyLogger

log = MyLogger.__call__().get_logger()


class TestCase1Alerts:
    def test_case_1_alerts(self):
        log.info("Testcase 1. Alerts")
        log.info("Шаг 1. Перейти на главную страницу")
        m_p = MainPage()
        m_p.open_page(settings["main_page_url"])
        assert m_p.page_opened(), "Страница не открыта"

        log.info("Шаг 2. Кликнуть на кнопку Alerts, Frame & Windows")
        m_p.click_alerts_frame_and_windows_btn()
        m_p.click_alerts_btn()
        assert m_p.alerts_form_on_page(), "На странице не появилась форма Alerts"

        log.info("Шаг 3. Нажать на кнопку Click Button to see alert")
        m_p.click_alert_btn_click_me()
        assert m_p.get_alert_text() == "You clicked a button", "Alert с текстом 'You clicked...' не открыт"

        log.info("Шаг 4. Нажать на кнопку OK (закрыть alert)")
        m_p.accept_alert()
        assert m_p.check_alert_closed(), "Alert не закрылся"

        log.info("Шаг 5. Нажать на кнопку On button click, confirm box will appear")
        m_p.click_alert_btn_confirm_box()
        assert m_p.get_alert_text() == "Do you confirm action?", "Alert с текстом 'Do you confirm...' не открыт"

        log.info("Шаг 6. Нажать на кнопку OK (закрыть alert)")
        m_p.accept_alert()
        assert m_p.check_alert_closed() is True, "Alert не закрылся"

        log.info("Шаг 7. Нажать на кнопку On button click, prompt box will appear")
        m_p.click_alert_btn_prompt_box()
        assert m_p.get_alert_text() == "Please enter your name"

        log.info("Шаг 8. Ввести случайно сгенерированный текст, нажать на кнопку ок (закрыть alert)")
        m_p.send_keys_to_prompt_box(random_string := gen_random_string(10))
        m_p.accept_alert()
        assert m_p.check_alert_closed() is True, "Alert не закрылся"
        assert random_string in m_p.get_prompt_result_text(), "Текст не соответствует введённому в prompt"
