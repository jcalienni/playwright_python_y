import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="function", autouse=True)
def start_test(page: Page):
    page.goto("https://the-internet.herokuapp.com/")
    yield
