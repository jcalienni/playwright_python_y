import re
from playwright.sync_api import Page, expect


def test_verify_title(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    expect(page).to_have_title("The Internet")


def test_verify_checkboxes_url(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    page.get_by_role("link", name="Checkboxes").click()

    expect(page).to_have_url("https://the-internet.herokuapp.com/checkboxes")


def test_verify_checkboxes_check(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    page.get_by_role("link", name="Checkboxes").click()
    page.get_by_role("checkbox").first.check()
    expect(page.get_by_role("checkbox").first).to_be_checked()


def test_verify_checkboxes_uncheck(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    page.get_by_role("link", name="Checkboxes").click()
    page.get_by_role("checkbox").nth(1).uncheck()
    expect(page.get_by_role("checkbox").nth(1)).not_to_be_checked()


def test_verify_input_text(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    page.get_by_role("link", name="Inputs").click()
    page.locator("input").fill("123")
    expect(page.locator("input")).to_have_value("123")


def test_verify_text_in_page(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    page.get_by_role("heading", name="Available Examples")
    expect(page.get_by_role("heading", name="Available Examples")
           ).to_contain_text("able")
    expect(page.get_by_role("heading", name="Available Examples")
           ).to_have_text("Available Examples")
