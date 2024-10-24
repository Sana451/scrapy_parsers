from ...config import settings
from ..pages.main_page import MainPage
from ...framework.logger import MyLogger

log = MyLogger.__call__().get_logger()


class TestCase2Iframe:
    def test_case_2_iframe(self):
        log.info("Testcase 2. Iframe")
        log.info("Шаг 1. Перейти на главную страницу")
        m_p = MainPage()
        m_p.open_page(settings["main_page_url"])
        assert m_p.page_opened(), "Страница не открыта"

        log.info("Шаг 2. Кликнуть на кнопку 'Alerts, Frame & Windows', кликнуть пункт 'Nested Frames'")
        m_p.click_alerts_frame_and_windows_btn()
        m_p.click_nested_frames_btn()
        assert m_p.frames_form_on_page(), "Страница с формой Nested Frames не открыта"
        assert 'Parent frame' in m_p.get_parent_frame_text(), "В центре страницы отсутствует надпись 'Parent frame'"
        assert 'Child Iframe' in m_p.get_child_frame_text(), "В центре страницы отсутствует надпись 'Child Iframe'"

        log.info("Шаг 3. В левом меню выбрать пункт 'Frames'")
        m_p.click_frames_btn()
        assert m_p.get_upper_frame_text() == m_p.get_lower_frame_text(), "Надпись верхнего фрейма не соотв. нижнему"
