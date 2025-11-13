from typing import TYPE_CHECKING
from playwright.sync_api import Page, Locator, expect
from pydantic import AnyHttpUrl
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from typing import Self

if TYPE_CHECKING:
    from loguru._logger import Logger


class BasePage:
    def __init__(self, page: Page, base_url: AnyHttpUrl, logger: "Logger"):
        self.page = page
        self.base_url = base_url
        self.logger = logger

    def open(self, path: str = "") -> Self:
        url = f"{self.base_url}{path}"
        self.logger.info(f"[{self.__class__.__name__}] Opening {url}")
        self.page.goto(url)
        return self

    def click(self, target: str | Locator, description: str = ""):
        """Click either a Locator or a string Selector."""
        try:
            description = description or str(target)

            if isinstance(target, Locator):
                target.click()
            else:
                self.page.click(target)
            self.logger.info(f"[{self.__class__.__name__}] Clicked {description}.")
        except PlaywrightTimeoutError as e:
            self.logger.error(f"[{self.__class__.__name__}] Failed to click {description} -> {e}")
            raise

    def fill(self, target: str | Locator, value: str, description: str = ""):
        """Fill input using a Locator or a string Selector."""
        try:
            description = description or str(target)

            if isinstance(target, Locator):
                target.fill(value)
            else:
                self.page.fill(target, value)
            self.logger.info(f"[{self.__class__.__name__}] Filled {description} with {value}.")
        except PlaywrightTimeoutError as e:
            self.logger.error(f"[{self.__class__.__name__}] Failed to fill {description} with {value} -> {e}")
            raise

    def wait_until_visible(self, target: str | Locator, timeout_seconds: int = 5, description: str = ""):
        """Wait for an element to be visible."""
        timeout_milliseconds = timeout_seconds * 1000
        description = description or str(target)
        if isinstance(target, Locator):
            target.wait_for(state="visible", timeout=timeout_milliseconds)
        else:
            self.page.wait_for_selector(selector=target, state="visible", timeout=timeout_milliseconds)
        self.logger.debug(f"[{self.__class__.__name__}] Element is visible: {description}")

    def assert_visible(self, target: str | Locator,  description: str = ""):
        description = description or str(target)
        if isinstance(target, Locator):
            expect(target).to_be_visible()
        else:
            expect(self.page.locator(target)).to_be_visible()
        self.logger.debug(f"[{self.__class__.__name__}] Verified element visible: {description}")

    def assert_url(self, path: str = ""):
        url = f"{self.base_url}{path}"
        expect(self.page).to_have_url(url)
        self.logger.debug(f"[{self.__class__.__name__}] Verified page`s url: {url}")
    

        
