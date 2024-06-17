import re
from playwright.sync_api import Page, expect

def test_verify_title(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    expect(page).to_have_title("The Internet")
    # assert page.title() == "The Internet"

def test_verify_checkboxes_url(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    page.get_by_role("link", name="Checkboxes").click()

    expect(page).to_have_url("https://the-internet.herokuapp.com/checkboxes")
    # assert page.url == "https://the-internet.herokuapp.com/checkboxes"