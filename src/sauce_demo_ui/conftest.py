import pytest
from src.sauce_demo_ui.utils.ui_settings import UiSettings
from src.common.helpers.config_manager import ConfigManager
from src.sauce_demo_ui.utils.logger import logger
from typing import TYPE_CHECKING
from pytest import FixtureRequest

if TYPE_CHECKING:
    from loguru._logger import Logger


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": False
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080}
    }

@pytest.fixture(scope="session")
def settings() -> UiSettings:
    return ConfigManager().ui()

@pytest.fixture(scope="session")
def ui_logger() -> "Logger":
    """Provides the logger for the entire test session."""
    logger.info("Setting up logger for the entire test session.")
    return logger

@pytest.fixture(autouse=True)
def log_test_start_end(request: FixtureRequest, ui_logger: "Logger"):
     ui_logger.info(f"=== START TEST: {request.node.name} ===")
     yield
     ui_logger.info(f"=== END TEST: {request.node.name} ===")