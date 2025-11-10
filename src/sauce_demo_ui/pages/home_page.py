from typing import Self
from playwright.sync_api import Locator, Page
from sauce_demo_ui.utils.log_action import log_step
from src.sauce_demo_ui.pages.login_page import LoginPage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru._logger import Logger


class HomePage:
    def __init__(self, page: Page, logger: "Logger"):
        self.page = page
        self.logger = logger

    @property
    def login_link(self) -> Locator:
        return self.page.get_by_role(role="link", name="Log In")

    @log_step("Navigating to login page via link on the home page.")
    def navigate_to_login_page(self) -> LoginPage:
        self.login_link.click()
        return LoginPage(self.page, self.logger)

    @log_step("Navigating to home page")
    def navigate(self, home_page_url) -> Self:
        self.page.goto(home_page_url)
        return self