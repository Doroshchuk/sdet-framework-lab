import pytest
from src.common.helpers.config_manager import ConfigManager
from src.sauce_demo_ui.pages.home_page import HomePage
from src.sauce_demo_ui.utils.ui_settings import UiSettings
from playwright.sync_api import Page


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

@pytest.fixture(scope="session")
def settings() -> UiSettings:
    return ConfigManager().ui()

def test_navigation_to_login_page_success(page: Page, settings: UiSettings):
    home_page = HomePage(page)
    home_page.navigate(settings.base_url)
    home_page.navigate_to_login_page().assert_loaded(settings.base_url)