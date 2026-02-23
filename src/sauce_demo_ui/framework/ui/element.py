from dataclasses import dataclass
from playwright.sync_api import Locator


@dataclass(frozen=True, eq=False)
class UiElement:
    locator: Locator
    description: str

    def __str__(self) -> str:
        return self.description