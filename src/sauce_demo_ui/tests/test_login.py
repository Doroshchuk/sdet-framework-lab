from sauce_demo_ui.utils.log_action import log_flow
from src.sauce_demo_ui.pages.home_page import HomePage
from src.sauce_demo_ui.utils.ui_settings import UiSettings
from playwright.sync_api import Page
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru._logger import Logger

@log_flow("Check navigation from the home page to login.")
def test_navigation_to_login_page_success(page: Page, settings: UiSettings, ui_logger: "Logger"):
    home_page = HomePage(page, settings.base_url, ui_logger)
    home_page.open()
    home_page.navigate_to_login_page().assert_loaded()