import pytest

from ..framework.browser import Driver


@pytest.fixture(autouse=True)
def get_browser_fixture(pytestconfig):
    Driver(pytestconfig.getoption('browser_name')).get_driver()
    yield
    Driver().del_driver()


@pytest.fixture(scope="session")
def name(pytestconfig):
    return pytestconfig.getoption("browser_name")


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome")
