import os
from playwright.sync_api import Page, expect, Playwright


def test_verify_title(page_herokuapp: Page):
    expect(page_herokuapp).to_have_title("The Internet")


def test_verify_checkboxes_url(page_herokuapp: Page):
    page_herokuapp.get_by_role("link", name="Checkboxes").click()

    expect(page_herokuapp).to_have_url(
        "https://the-internet.herokuapp.com/checkboxes")


def test_verify_checkboxes_check(page_herokuapp: Page):
    page_herokuapp.get_by_role("link", name="Checkboxes").click()
    page_herokuapp.get_by_role("checkbox").first.check()
    # Take screenshot to element
    page_herokuapp.get_by_role("checkbox").first.screenshot(
        path="screenshots/test_example/test.png")
    expect(page_herokuapp.get_by_role("checkbox").first).to_be_checked()


def test_verify_checkboxes_uncheck(page_herokuapp: Page):
    page_herokuapp.get_by_role("link", name="Checkboxes").click()
    page_herokuapp.get_by_role("checkbox").nth(1).uncheck()
    expect(page_herokuapp.get_by_role("checkbox").nth(1)).not_to_be_checked()


def test_verify_input_text(page_herokuapp: Page):
    page_herokuapp.get_by_role("link", name="Inputs").click()
    page_herokuapp.locator("input").fill("123")
    expect(page_herokuapp.locator("input")).to_have_value("123")


def test_verify_text_in_page(page_herokuapp: Page):
    page_herokuapp.get_by_role("heading", name="Available Examples")
    expect(page_herokuapp.get_by_role("heading", name="Available Examples")
           ).to_contain_text("able")
    expect(page_herokuapp.get_by_role("heading", name="Available Examples")
           ).to_have_text("Available Examples")


def test_hover_element(page_herokuapp: Page):
    page_herokuapp.get_by_role("link", name="Hover").click()
    expect(page_herokuapp.get_by_role("link", name="View profile")
           ).not_to_be_visible()
    images = page_herokuapp.get_by_role("img", name="User Avatar")
    expect(images).to_have_count(3)
    page_herokuapp.get_by_role("img", name="User Avatar").first.hover()
    expect(page_herokuapp.get_by_role("link", name="View profile")
           ).to_be_visible()


def test_focus_element(page_herokuapp: Page):
    page_herokuapp.get_by_role("link", name="Horizontal Slider").click()
    page_herokuapp.get_by_role("slider").focus()
    page_herokuapp.get_by_role("slider").press("ArrowRight")
    expect(page_herokuapp.locator("#range")).to_have_text("0.5")


def test_dropdown_element(page_herokuapp: Page):
    page_herokuapp.get_by_role("link", name="Dropdown").click()
    page_herokuapp.locator("#dropdown").select_option("1")
    expect(page_herokuapp.locator("#dropdown > option:nth-child(2)")
           ).to_have_attribute("selected", "selected")


def test_enabled_disabled_element(page_herokuapp: Page):
    page_herokuapp.get_by_role("link", name="Dynamic Controls").click()
    expect(page_herokuapp.get_by_role("textbox")).to_be_disabled()
    page_herokuapp.get_by_role("button", name="Enable").click()
    expect(page_herokuapp.get_by_role("textbox")).to_be_enabled()


def test_basic_authentication(page_herokuapp: Page):
    page_herokuapp.goto(
        "https://admin:admin@the-internet.herokuapp.com/basic_auth")

    expect(page_herokuapp.locator("#content p")
           ).to_have_text("Congratulations! You must have the proper credentials.")


def test_form_authentication(page_herokuapp: Page):
    page_herokuapp.get_by_role("link", name="Form Authentication").click()

    page_herokuapp.get_by_label("Username").fill("tomsmith")
    page_herokuapp.get_by_label("Password").fill("SuperSecretPassword!")
    page_herokuapp.locator("button").click()
    expect(page_herokuapp.locator("h4")).to_have_text(
        "Welcome to the Secure Area. When you are done click logout below.")
    expect(page_herokuapp.locator("#flash")).to_contain_text(
        "You logged into a secure area!")


def test_video_playwright(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=True)

    video_context = browser.new_context(
        record_video_dir="videos/",
        record_video_size={"width": 640, "height": 480}
    )
    page = video_context.new_page()

    page.goto("https://the-internet.herokuapp.com/")
    page.get_by_role("link", name="Dynamic Controls").click()
    expect(page.get_by_role("textbox")).to_be_disabled()
    page.get_by_role("button", name="Enable").click()
    expect(page.get_by_role("textbox")).to_be_enabled()

    video_context.close()


def test_two_pages(browser):
    context = browser.new_context()
    page1 = context.new_page()
    page2 = context.new_page()

    page1.goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    expect(page1.locator("#content p")
           ).to_have_text("Congratulations! You must have the proper credentials.")

    page2.goto("https://the-internet.herokuapp.com/basic_auth")
    expect(page1.locator("#content p")
           ).to_have_text("Congratulations! You must have the proper credentials.")


def test_two_differet_contexts(browser):
    context1 = browser.new_context()
    context2 = browser.new_context()
    page1 = context1.new_page()
    page2 = context2.new_page()

    page1.goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    expect(page1.locator("#content p")
           ).to_have_text("Congratulations! You must have the proper credentials.")

    page2.goto("https://the-internet.herokuapp.com")
    page2.get_by_role("link", name="Basic Auth").click()

    expect(page2.locator("#content p")).not_to_be_visible()


def test_download_file(page_herokuapp: Page):
    download_dir = 'resourses/downloads/'
    page_herokuapp.get_by_role(
        "link", name="File Download", exact=True).click()
    with page_herokuapp.expect_download() as download_info:
        page_herokuapp.get_by_role("link", name="test_text.txt").click()
    download = download_info.value
    download_file_dir = download_dir + download.suggested_filename
    download.save_as(download_file_dir)
    assert os.path.isfile(download_file_dir), f"{download.suggested_filename} file doesn't exists."
    os.remove(download_file_dir)


def test_upload_file(page_herokuapp: Page):
    page_herokuapp.get_by_role("link", name="File Upload").click()
    test_filte_name = 'test_text.txt'
    page_herokuapp.locator(
        "#file-upload").set_input_files(f'resourses/test_files/{test_filte_name}')
    page_herokuapp.locator("#file-submit").click()

    expect(page_herokuapp.get_by_role("heading", name="File Uploaded!")
           ).to_have_text("File Uploaded!")
    expect(page_herokuapp.locator('#uploaded-files')
           ).to_have_text(test_filte_name)
    
