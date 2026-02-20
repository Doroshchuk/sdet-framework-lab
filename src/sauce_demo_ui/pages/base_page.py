from __future__ import annotations
from typing import TYPE_CHECKING
from common.utils.log_action import LogLevelType
from playwright.sync_api import Page, Locator, expect
from pydantic import AnyHttpUrl
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from typing import Self
from sauce_demo_ui.utils.log_action import log_step

if TYPE_CHECKING:
    from loguru import Logger


class BasePage:
    def __init__(self, page: Page, base_url: AnyHttpUrl, logger: Logger):
        self.page = page
        self.base_url = base_url
        self.logger = logger

    @log_step(lambda self, *args, path="", **kwargs: f"Opening {self.base_url}{path}.")
    def open(self, path: str = "") -> Self:
        self.page.goto(f"{self.base_url}{path}")
        return self

    @log_step(lambda self, target, *args, description=None, **kwargs: f"Clicking {self._describe(target, description)}.")
    def click(self, target: str | Locator, description: str = None) -> Self:
        """Click either a Locator or a string Selector."""
        
        description = self._describe(target, description)
        try:
            if isinstance(target, Locator):
                target.click()
            else:
                self.page.click(target)
            self.logger.debug(f"[{self.__class__.__name__}] Click succeeded: {description}")
            return self
        except PlaywrightTimeoutError as e:
            self.logger.error(
                f"[{self.__class__.__name__}] Failed to click {description} → {e}"
            )
            raise

    @log_step(lambda self, target, value, *args, description=None, **kwargs: f"Filling {self._describe(target, description)} with {value}.")
    def fill(self, target: str | Locator, value: str, description: str = None) -> Self:
        """Fill input using a Locator or a string Selector."""

        description = self._describe(target, description)
        try:
            if isinstance(target, Locator):
                target.fill(value)
            else:
                self.page.fill(target, value)
            self.logger.debug(f"[{self.__class__.__name__}] Fill succeeded: {description}")
            return self
        except PlaywrightTimeoutError as e:
            self.logger.error(
                f"[{self.__class__.__name__}] Failed to fill {description} with {value} → {e}"
            )
            raise

    @log_step(lambda self, target, *args, description=None, **kwargs: f"Waiting for {self._describe(target, description)} to be visible.", level=LogLevelType.DEBUG)
    def wait_until_visible(self, target: str | Locator, timeout_seconds: int = 5, description: str = None) -> Self:
        """Wait for an element to be visible."""
        
        timeout_milliseconds = timeout_seconds * 1000
        description = self._describe(target, description)
        try:
            if isinstance(target, Locator):
                target.wait_for(state="visible", timeout=timeout_milliseconds)
            else:
                self.page.wait_for_selector(selector=target, state="visible", timeout=timeout_milliseconds)
            self.logger.debug(f"[{self.__class__.__name__}] Wait succeeded: {description}")
            return self
        except PlaywrightTimeoutError as e:
            self.logger.error(
                f"[{self.__class__.__name__}] Timeout while waiting for {description} to be visible → {e}"
            )
            raise

    @log_step(lambda self, target, *args, description=None, **kwargs: f"Asserting {self._describe(target, description)} is visible.")
    def assert_visible(self, target: str | Locator,  description: str = None) -> Self:
        description = self._describe(target, description)
        try:
            if isinstance(target, Locator):
                expect(target).to_be_visible()
            else:
                expect(self.page.locator(target)).to_be_visible()
            return self
        except PlaywrightTimeoutError as e:
            self.logger.error(f"[{self.__class__.__name__}] Timeout while waiting for element: {description} → {e}")
            raise

    @log_step(lambda self, *args, path="", **kwargs: f"Asserting page`s url is {self.base_url}{path}.")
    def assert_url(self, path: str = "") -> Self:
        url = f"{self.base_url}{path}"
        try:
            expect(self.page).to_have_url(url)
            return self
        except PlaywrightTimeoutError as e:
            self.logger.error(f"[{self.__class__.__name__}] Timeout while waiting for url: {url} → {e}")
            raise
    
    def _describe(self, target: str | Locator, description: str = None):
        if description:
            return description
        if isinstance(target, Locator):
            internal_selector = getattr(getattr(target, "_impl_obj", None), "_selector", None)
            if internal_selector:
                return internal_selector
        return str(target)