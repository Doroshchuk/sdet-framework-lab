import pytest
from src.sauce_demo_ui.utils.ui_settings import UiSettings
from src.common.helpers.config_manager import ConfigManager


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