from __future__ import annotations
from pathlib import Path
import time
import pytest
from common.helpers.config_manager import ConfigManager
from common.helpers.enums import SettingsTypeEnum
from sauce_demo_ui.framework.config.ui_settings import UiSettings
from sauce_demo_ui.framework.logging.logger import logger
from typing import TYPE_CHECKING, Any
from pytest import CallInfo, FixtureRequest, Item, TestReport
from collections.abc import Generator

if TYPE_CHECKING:
    from loguru import Logger


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, settings: UiSettings) -> dict:
    return {
        **browser_type_launch_args,
        "channel": settings.browser_channel,
        "headless": settings.headless,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, settings: UiSettings) -> dict:
    return {**browser_context_args, "viewport": settings.viewport.model_dump()}


@pytest.fixture(scope="session")
def settings() -> UiSettings:
    return ConfigManager.load(
        env_var="SETTINGS_PATH_UI",
        default_path="config/settings.sauce_demo_ui.json",
        settings_type=SettingsTypeEnum.UI,
        parser=lambda data: UiSettings(**data).normalized(),
    )


@pytest.fixture(scope="session")
def ui_logger() -> Logger:
    """Provides the logger for the entire test session."""
    logger.info("Initializing test session logger.")
    return logger


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: Item, call: CallInfo[None]) -> Generator[None, Any, None]:
    outcome = yield
    report: TestReport = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def log_test_start_end(request: FixtureRequest, ui_logger: Logger) -> Generator[None, None, None]:
    test_name = request.node.name
    artifacts_dir = request.config.rootpath / "test-results"
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

    if status.startswith("FAILED"):
        test_artifacts_dir = _find_latest_test_artifacts_dir(artifacts_dir)
        ui_logger.error(
            f"Open artifacts retained by pytest-playwright in Finder: open {artifacts_dir.resolve()}"
        )

        if test_artifacts_dir is not None:
            ui_logger.error(
                f"Latest test artifacts dir: {test_artifacts_dir.resolve()}"
            )
            artifacts = _find_artifacts_for_test(test_artifacts_dir)

            for trace_file in artifacts["traces"]:
                ui_logger.error(
                    f"Open trace: playwright show-trace {trace_file.resolve()}"
                )

            for screenshot_file in artifacts["screenshots"]:
                ui_logger.error(f"Open screenshot: open {screenshot_file.resolve()}")

            for video_file in artifacts["videos"]:
                ui_logger.error(f"Open video: open {video_file.resolve()}")


def _find_latest_test_artifacts_dir(root_artifacts_dir: Path) -> Path | None:
    if not root_artifacts_dir.exists():
        return None

    candidate_dirs = [path for path in root_artifacts_dir.iterdir() if path.is_dir()]
    if not candidate_dirs:
        return None

    return max(candidate_dirs, key=lambda path: path.stat().st_mtime)


def _find_artifacts_for_test(test_artifacts_dir: Path) -> dict[str, list[Path]]:
    artifacts_dict: dict[str, list[Path]] = {"traces": [], "screenshots": [], "videos": []}

    if not test_artifacts_dir.exists():
        return artifacts_dict

    for file_path in test_artifacts_dir.glob("*"):
        if not file_path.is_file():
            continue

        file_name_lower = file_path.name.lower()
        file_suffix_lower = file_path.suffix.lower()
        if file_suffix_lower == ".zip" and "trace" in file_name_lower:
            artifacts_dict["traces"].append(file_path)
        elif file_suffix_lower == ".png":
            artifacts_dict["screenshots"].append(file_path)
        elif file_suffix_lower == ".webm":
            artifacts_dict["videos"].append(file_path)

    return artifacts_dict
