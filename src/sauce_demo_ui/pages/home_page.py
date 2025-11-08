from typing import Self
from playwright.sync_api import Locator, Page
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

    def navigate_to_login_page(self) -> LoginPage:
        self.logger.info(f"Navigating to login page via link on thehome page.")
        self.login_link.click()
        return LoginPage(self.page, self.logger)

    def navigate(self, home_page_url) -> Self:
        self.logger.info(f"Navigating to home page: {home_page_url}")
        self.page.goto(home_page_url)
        return self