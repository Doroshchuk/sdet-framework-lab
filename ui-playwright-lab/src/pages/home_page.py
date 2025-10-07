from typing import Self
from playwright.sync_api import Locator, Page
from src.pages.login_page import LoginPage


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def login_link(self) -> Locator:
        return self.page.get_by_role(role="link", name="Log In")

    def navigate_to_login_page(self) -> LoginPage:
        self.login_link.click()
        return LoginPage(self.page)

    def navigate(self, home_page_url) -> Self:
        self.page.goto(home_page_url)
        return self