from __future__ import annotations
from sauce_demo_ui.pages.base_page import BasePage
from sauce_demo_ui.utils.log_action import log_step
from typing import Self
from playwright.sync_api import Locator, Page, expect
from pydantic import AnyHttpUrl
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru._logger import Logger


class LoginPage(BasePage):
    path = "/account/login"

    def __init__(self, page: Page, base_url: AnyHttpUrl, logger: Logger):
        super().__init__(page, base_url, logger)

    @property
    def email_input(self) -> Locator:
        return self.page.get_by_label("Email Address")

    @log_step("Asserting login page is loaded.")
    def assert_loaded(self) -> Self:
        self.assert_url(self.path)
        self.assert_visible(self.email_input)
        return self