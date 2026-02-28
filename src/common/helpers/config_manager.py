import json
import os
from pathlib import Path
from common.helpers.enums import SettingsTypeEnum
from typing import Callable, TypeVar

SettingsType = TypeVar("SettingsType")

class ConfigManager:
    _settings: dict[SettingsTypeEnum, object] = {}

    @classmethod
    def load(
        cls, 
        *,
        env_var: str,
        default_path: str,
        settings_type: SettingsTypeEnum,
        parser: Callable[[dict], SettingsType]
        ) -> SettingsType:
        if settings_type in cls._settings:
            return cls._settings[settings_type]

        path_str = os.getenv(env_var, default_path)
        path = Path(path_str if Path(path_str).is_absolute() else Path.cwd() / path_str)
        if not path.exists():
            raise FileNotFoundError(f"{settings_type} settings not found at {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        if not data:
            raise ValueError(f"Empty {settings_type} settings JSON at {path}")

        settings = parser(data)

        cls._settings[settings_type] = settings
        return settings