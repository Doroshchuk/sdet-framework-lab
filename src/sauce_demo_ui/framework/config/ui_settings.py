from pydantic import BaseModel, Field, AnyHttpUrl
from typing import Optional, Self
from src.common.helpers.enums import EnvironmentEnum


class Viewport(BaseModel):
    width: int = 1920
    height: int = 1080

class UiSettings(BaseModel):
    env: EnvironmentEnum = EnvironmentEnum.LOCAL
    base_url: AnyHttpUrl
    headless: bool = True
    channel: Optional[str] = None
    viewport: Viewport = Field(default_factory=Viewport)

    def normalized(self) -> Self:
        # remove trailing slash so URL joins don’t produce `//`
        return self.model_copy(update={"base_url": str(self.base_url).rstrip("/")})