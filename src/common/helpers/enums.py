from enum import Enum


class EnvironmentEnum(Enum):
    LOCAL = "local"
    CI = "ci"

class SettingsTypeEnum(Enum):
    UI = "UI"
    API = "API"