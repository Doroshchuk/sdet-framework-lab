from typing import Self
from playwright.sync_api import Locator, Page, expect


class LoginPage:
    path = "/account/login"

    def __init__(self, page: Page):
        self.page = page

    @property
    def email_input(self) -> Locator:
        return self.page.get_by_label("Email Address")

    def assert_loaded(self, base_url: str) -> Self:
        expect(self.page).to_have_url(f"{base_url}{self.path}")
        expect(self.email_input).to_be_visible()
        return self