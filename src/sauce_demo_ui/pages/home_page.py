from typing import Self
from playwright.sync_api import Locator, Page
from pydantic import AnyHttpUrl
from sauce_demo_ui.pages.base_page import BasePage
from sauce_demo_ui.utils.log_action import log_step
from src.sauce_demo_ui.pages.login_page import LoginPage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru._logger import Logger


class HomePage(BasePage):
    def __init__(self, page: Page, base_url: AnyHttpUrl, logger: "Logger"):
        super().__init__(page, base_url, logger)

    @property
    def login_link(self) -> Locator:
        return self.page.get_by_role(role="link", name="Log In")

    @log_step("Navigating to login page via link on the home page.")
    def navigate_to_login_page(self) -> LoginPage:
        self.click(self.login_link)
        return LoginPage(self.page, self.base_url, self.logger)

    def open(self) -> Self:
        super().open()
        return self