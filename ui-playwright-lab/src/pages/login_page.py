from typing import Self
from playwright.sync_api import Locator, Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def email_input(self) -> Locator:
        return self.page.get_by_label("Email Address")

    def assert_loaded(self, login_page_url) -> Self:
        expect(self.page).to_have_url(login_page_url)
        expect(self.email_input).to_be_visible()
        return self