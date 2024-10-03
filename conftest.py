import pytest
from playwright.sync_api import Page
import datetime


@pytest.fixture(scope="function")
def page_herokuapp(page: Page):
    page.goto("https://the-internet.herokuapp.com/")
    yield page


@pytest.fixture(scope="function")
def page_reqres(page: Page):
    page.goto("https://reqres.in/")
    yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Check if the test has failed
    if report.when == "call" and report.failed:
        page = item.funcargs['page']

        screenshot_path = f"screenshots/failed_tests/{item.name}-{datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.png"
        page.screenshot(path=screenshot_path)
