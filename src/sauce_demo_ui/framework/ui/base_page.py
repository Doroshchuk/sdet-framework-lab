from __future__ import annotations
from typing import TYPE_CHECKING
from playwright.sync_api import Page, expect
from pydantic import AnyHttpUrl
from typing import Self
from sauce_demo_ui.framework.logging.log_action import log_step, LogLevelType
from sauce_demo_ui.framework.ui.element import UiElement

if TYPE_CHECKING:
    from loguru import Logger


class BasePage:
    def __init__(self, page: Page, base_url: AnyHttpUrl, logger: Logger):
        self.page = page
        self.base_url = base_url
        self.logger = logger

    @log_step(lambda self, path="", **_: f"Opening {self.base_url}{path}.")
    def open(self, path: str = "") -> Self:
        self.page.goto(f"{self.base_url}{path}")
        return self

    @log_step(lambda self, element, **_: f"Clicking {element}.")
    def click(self, element: UiElement) -> Self:
        """Click a UiElement.locator."""

        element.locator.click()
        return self

    @log_step(lambda self, element, value, **_: f"Filling {element} with {value}.")
    def fill(self, element: UiElement, value: str) -> Self:
        """Fill input using a UiElement.locator."""

        element.locator.fill(value)
        return self

    @log_step(
        lambda self, element, timeout_seconds=5, **_: f"Waiting for {element} to be visible.",
        level=LogLevelType.DEBUG,
    )
    def wait_until_visible(self, element: UiElement, timeout_seconds: int = 5) -> Self:
        """Wait for a UiElement.locator to be visible."""

        timeout_milliseconds = timeout_seconds * 1000
        element.locator.wait_for(state="visible", timeout=timeout_milliseconds)
        return self

    @log_step(lambda self, element, **_: f"Asserting {element} is visible.")
    def assert_visible(self, element: UiElement) -> Self:
        """Assert a UiElement.locator is visible."""

        expect(element.locator).to_be_visible()
        return self

    @log_step(
        lambda self, path="", **_: f"Asserting page`s url is {self.base_url}{path}."
    )
    def assert_url(self, path: str = "") -> Self:
        """Assert a page`s url."""

        url = f"{self.base_url}{path}"
        expect(self.page).to_have_url(url)
        return self
