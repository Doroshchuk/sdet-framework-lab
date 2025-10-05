from playwright.sync_api import sync_playwright, expect


def test_navigation_to_login_page_success():
    homepage_url = "https://sauce-demo.myshopify.com"
    login_page_url = "https://sauce-demo.myshopify.com/account/login"
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()
        page.goto(homepage_url)

        login_link = page.get_by_role(role="link", name="Log In")
        email_input = page.get_by_label("Email Address")
        login_link.click()
        expect(page).to_have_url(login_page_url)
        expect(email_input).to_be_visible()

        browser.close()