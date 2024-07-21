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


def test_hover_element(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    page.get_by_role("link", name="Hover").click()
    expect(page.get_by_role("link", name="View profile")
           ).not_to_be_visible()
    images = page.get_by_role("img", name="User Avatar")
    expect(images).to_have_count(3)
    page.get_by_role("img", name="User Avatar").first.hover()
    expect(page.get_by_role("link", name="View profile")
           ).to_be_visible()


def test_focus_element(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    page.get_by_role("link", name="Horizontal Slider").click()
    page.get_by_role("slider").focus()
    page.get_by_role("slider").press("ArrowRight")
    expect(page.locator("#range")).to_have_text("0.5")


def test_dropdown_element(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    page.get_by_role("link", name="Dropdown").click()
    page.locator("#dropdown").select_option("1")
    expect(page.locator("#dropdown > option:nth-child(2)")
           ).to_have_attribute("selected", "selected")


def test_enabled_disabled_element(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    page.get_by_role("link", name="Dynamic Controls").click()
    expect(page.get_by_role("textbox")).to_be_disabled()
    page.get_by_role("button", name="Enable").click()
    expect(page.get_by_role("textbox")).to_be_enabled()
