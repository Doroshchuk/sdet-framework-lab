from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru._logger import Logger

class ActionType:
    FLOW = "flow"
    STEP = "step"


def make_log_action(logger: "Logger", action: ActionType):
    def log_action(description: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                logger.info(f"[{str(action)}]: {description}")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    return log_action
