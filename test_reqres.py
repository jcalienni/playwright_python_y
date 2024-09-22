from playwright.sync_api import Page, expect


def test_wait_api(page_reqres: Page):
    with page_reqres.expect_request("**/api/users?delay=3"):
        page_reqres.locator('li[data-id="delay"]').click()
    expect(page_reqres.locator(
        'pre[data-key="output-response"]')).to_contain_text("george.bluth")
