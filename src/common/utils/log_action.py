from __future__ import annotations
from functools import wraps
from typing import TYPE_CHECKING, Callable
from enum import Enum

if TYPE_CHECKING:
    from loguru import Logger

class LogActionType(Enum):
    FLOW = "flow"
    STEP = "step"

class LogLevelType(Enum):
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

def make_log_action(logger: Logger, action: LogActionType):
    def log_action(description: str | Callable, level: LogLevelType = LogLevelType.INFO):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if callable(description):
                    try:
                        # Pass the same args the method receives
                        msg = description(*args, **kwargs)
                    except TypeError as e:
                        logger.warning(
                            f"[{action.value.upper()}] Message builder failed for {func.__name__}: {e}. "
                            "Falling back to function name."
                        )
                        msg = f"{func.__name__}()"     # fallback
                else:
                    msg = description

                # Run function
                try:
                    logger.log(level.value.upper(), f"[{action.value.upper()}]: {msg}")
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"[{action.value.upper()} FAILED] {msg} → {e}")
                    raise
            return wrapper
        return decorator
    return log_action
