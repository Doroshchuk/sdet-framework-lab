from src.sauce_demo_ui.pages.home_page import HomePage
from src.sauce_demo_ui.utils.ui_settings import UiSettings
from playwright.sync_api import Page

def test_navigation_to_login_page_success(page: Page, settings: UiSettings):
    home_page = HomePage(page)
    home_page.navigate(settings.base_url)
    home_page.navigate_to_login_page().assert_loaded(settings.base_url)