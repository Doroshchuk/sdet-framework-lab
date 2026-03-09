from __future__ import annotations
import time
import pytest
from common.helpers.config_manager import ConfigManager
from common.helpers.enums import SettingsTypeEnum
from sauce_demo_ui.framework.config.ui_settings import UiSettings
from sauce_demo_ui.framework.logging.logger import logger
from typing import TYPE_CHECKING
from pytest import CallInfo, FixtureRequest, Item, TestReport

if TYPE_CHECKING:
    from loguru import Logger


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, settings: UiSettings) -> dict:
    return {
        **browser_type_launch_args,
        "channel": settings.browser_channel,
        "headless": settings.headless
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, settings: UiSettings) -> dict:
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
    logger.info("Initializing test session logger.")
    return logger

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: Item, call: CallInfo[None]) -> None:
    outcome = yield
    report: TestReport = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

@pytest.fixture(autouse=True)
def log_test_start_end(request: FixtureRequest, ui_logger: Logger) -> None:
    test_name = request.node.name
    start_time = time.perf_counter()

    ui_logger.info(f"=== START TEST: {test_name} ===")
    yield

    duration_seconds = time.perf_counter() - start_time

    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    rep_teardown = getattr(request.node, "rep_teardown", None)

    if rep_setup and rep_setup.failed:
        status = "FAILED_IN_SETUP"
    elif rep_call and rep_call.failed:
        status = "FAILED"
    elif rep_teardown and rep_teardown.failed:
        status = "FAILED_IN_TEARDOWN"
    elif (rep_setup and rep_setup.skipped) or (rep_call and rep_call.skipped):
        status = "SKIPPED"
    else:
        status = "PASSED"

    ui_logger.info(
        f"=== END TEST: {test_name} | STATUS: {status} "
        f"| DURATION: {duration_seconds:.2f}s ==="
        )