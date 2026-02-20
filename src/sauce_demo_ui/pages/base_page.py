from __future__ import annotations
from typing import TYPE_CHECKING
from common.utils.log_action import LogLevelType
from playwright.sync_api import Page, Locator, expect
from pydantic import AnyHttpUrl
from typing import Self
from sauce_demo_ui.utils.log_action import log_step

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

    @log_step(lambda self, target, description=None, **_: f"Clicking {self._describe(target, description)}.")
    def click(self, target: str | Locator, description: str | None = None) -> Self:
        """Click either a Locator or a string Selector."""
        
        if isinstance(target, Locator):
            target.click()
        else:
            self.page.click(target)
        return self

    @log_step(lambda self, target, value, description=None, **_: f"Filling {self._describe(target, description)} with {value}.")
    def fill(self, target: str | Locator, value: str, description: str | None = None) -> Self:
        """Fill input using a Locator or a string Selector."""

        if isinstance(target, Locator):
            target.fill(value)
        else:
            self.page.fill(target, value)
        return self

    @log_step(lambda self, target, timeout_seconds=5, description=None, **_: f"Waiting for {self._describe(target, description)} to be visible.", level=LogLevelType.DEBUG)
    def wait_until_visible(self, target: str | Locator, timeout_seconds: int = 5, description: str | None = None) -> Self:
        """Wait for an element to be visible."""
        
        timeout_milliseconds = timeout_seconds * 1000
        if isinstance(target, Locator):
            target.wait_for(state="visible", timeout=timeout_milliseconds)
        else:
            self.page.wait_for_selector(selector=target, state="visible", timeout=timeout_milliseconds)
        return self

    @log_step(lambda self, target, description=None, **_: f"Asserting {self._describe(target, description)} is visible.")
    def assert_visible(self, target: str | Locator,  description: str | None = None) -> Self:
        """Assert an element is visible."""

        if isinstance(target, Locator):
            expect(target).to_be_visible()
        else:
            expect(self.page.locator(target)).to_be_visible()
        return self

    @log_step(lambda self, path="", **_: f"Asserting page`s url is {self.base_url}{path}.")
    def assert_url(self, path: str = "") -> Self:
        """Assert a page`s url."""
        
        url = f"{self.base_url}{path}"
        expect(self.page).to_have_url(url)
        return self
    
    def _describe(self, target: str | Locator, description: str | None = None) -> str:
        if description:
            return description
        # best-effort: Playwright private internals, may change between versions
        if isinstance(target, Locator):
            internal_selector = getattr(getattr(target, "_impl_obj", None), "_selector", None)
            if internal_selector:
                return internal_selector
        return str(target)