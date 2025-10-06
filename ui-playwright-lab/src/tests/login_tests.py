from playwright.sync_api import sync_playwright, expect
import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": False
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080}
    }

def test_navigation_to_login_page_success(page):
    homepage_url = "https://sauce-demo.myshopify.com"
    login_page_url = "https://sauce-demo.myshopify.com/account/login"
    
    page.goto(homepage_url)

    login_link = page.get_by_role(role="link", name="Log In")
    email_input = page.get_by_label("Email Address")
    login_link.click()
    expect(page).to_have_url(login_page_url)
    expect(email_input).to_be_visible()