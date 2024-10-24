from ...config import settings
from ..pages.main_page import MainPage
from ...framework.logger import MyLogger

log = MyLogger.__call__().get_logger()


class TestCase4Handles:
    def test_case_4_handles(self):
        log.info("Testcase 4. Handles")
        log.info("Шаг 1. Перейти на главную страницу")
        m_p = MainPage()
        m_p.open_page(settings["main_page_url"])
        assert m_p.page_opened(), "Страница не открыта"

        log.info("Шаг 2. Кликнуть на кнопку 'Alerts, Frame & Windows', кликнуть пункт 'Browser Windows'")
        m_p.click_alerts_frame_and_windows_btn()
        m_p.click_browser_windows_btn()
        assert m_p.browser_windows_form_on_page(), "Страница с формой 'Browser Windows' не открыта"

        log.info("Шаг 3. Кликнуть на кнопку 'New Tab'")
        tabs_count_before_open_new_tab = m_p.tabs_count()
        m_p.click_new_tab_btn()
        assert m_p.tabs_count() > tabs_count_before_open_new_tab, "Новая вкладка браузера не открылась"
        assert m_p.sample_text_on_page(), "Вкладка не содержит текста 'sample page'"

        log.info("Шаг 4. Закрыть текущую вкладку")
        m_p.close_current_tab()
        assert m_p.browser_windows_form_on_page(), "Страница с формой 'Browser Windows' не открыта"

        log.info("Шаг 5. В левом меню выбрать 'Elements' → 'Links'")
        m_p.click_elements_btn()
        m_p.click_links_btn()
        assert m_p.links_form_on_page(), "Страница с формой 'Links' не открыта"
        tabs_count_before_open_new_tab = m_p.tabs_count()

        log.info("Шаг 6. Перейти по ссылке 'Home'")
        m_p.click_home_link()
        assert m_p.tabs_count() > tabs_count_before_open_new_tab, "Новая вкладка браузера не открылась"
        assert m_p.page_opened(), "Новая вкладка открыта не главной странице"

        log.info("Шаг 7. Переключиться на предыдущую вкладку")
        m_p.switch_to_default_tab()
        assert m_p.links_form_on_page(), "Страница с формой 'Links' не открыта"
