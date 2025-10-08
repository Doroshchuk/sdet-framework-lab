import json
import os
from pathlib import Path
from src.sauce_demo_ui.utils.ui_settings import UiSettings
from typing import Optional


class ConfigManager:
    _ui_cache: Optional[UiSettings] = None

    @classmethod
    def ui(cls) -> UiSettings:
        if cls._ui_cache is not None:
            return cls._ui_cache

        path_str = os.getenv("SETTINGS_PATH_UI", "config/settings.sauce_demo_ui.json")
        path = Path(path_str if Path(path_str).is_absolute() else Path.cwd() / path_str)
        if not path.exists():
            raise FileNotFoundError(f"UI settings not found at {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        if not data:
            raise ValueError(f"Empty UI settings JSON at {path}")

        settings = UiSettings(**data).normalized()

        cls._ui_cache = settings
        return settings