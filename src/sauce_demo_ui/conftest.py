from __future__ import annotations
import pytest
from common.helpers.config_manager import ConfigManager
from common.helpers.enums import SettingsTypeEnum
from sauce_demo_ui.framework.config.ui_settings import UiSettings
from sauce_demo_ui.framework.logging.logger import logger
from typing import TYPE_CHECKING
from pytest import FixtureRequest

if TYPE_CHECKING:
    from loguru import Logger


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, settings: UiSettings):
    return {
        **browser_type_launch_args,
        "channel": settings.browser_channel,
        "headless": settings.headless
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, settings: UiSettings):
    return {
        **browser_context_args,
        "viewport": settings.viewport.model_dump()
    }

@pytest.fixture(scope="session")
def settings() -> UiSettings:
    return ConfigManager.load(
        env_var="SETTINGS_PATH_UI",
        default_path="config/settings.sauce_demo_ui.json",
        settings_type=SettingsTypeEnum.UI,
        parser=lambda data: UiSettings(**data).normalized()
    )

@pytest.fixture(scope="session")
def ui_logger() -> Logger:
    """Provides the logger for the entire test session."""
    logger.info("Setting up logger for the entire test session.")
    return logger

@pytest.fixture(autouse=True)
def log_test_start_end(request: FixtureRequest, ui_logger: Logger):
     ui_logger.info(f"=== START TEST: {request.node.name} ===")
     yield
     ui_logger.info(f"=== END TEST: {request.node.name} ===")