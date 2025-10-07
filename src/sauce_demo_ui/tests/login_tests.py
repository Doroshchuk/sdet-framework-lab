from playwright.sync_api import sync_playwright, expect
import pytest
from src.sauce_demo_ui.pages.home_page import HomePage


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
    home_page_url = "https://sauce-demo.myshopify.com"
    login_page_url = "https://sauce-demo.myshopify.com/account/login"
    
    home_page = HomePage(page)
    home_page.navigate(home_page_url)
    home_page.navigate_to_login_page().assert_loaded(login_page_url)