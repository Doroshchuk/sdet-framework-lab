from sauce_demo_ui.utils.log_action import log_step
from typing import Self
from playwright.sync_api import Locator, Page, expect
from pydantic import AnyHttpUrl
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru._logger import Logger


class LoginPage:
    path = "/account/login"

    def __init__(self, page: Page, logger: "Logger"):
        self.page = page
        self.logger = logger

    @property
    def email_input(self) -> Locator:
        return self.page.get_by_label("Email Address")

    @log_step("Asserting login page is loaded.")
    def assert_loaded(self, base_url: AnyHttpUrl) -> Self:
        expect(self.page).to_have_url(f"{base_url}{self.path}")
        expect(self.email_input).to_be_visible()
        return self