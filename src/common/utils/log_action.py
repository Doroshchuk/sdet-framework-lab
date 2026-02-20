from __future__ import annotations
from functools import wraps
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from loguru import Logger

class LogActionType:
    FLOW = "flow"
    STEP = "step"

class LogLevelType:
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
                    except Exception:
                        msg = f"{func.__name__}()"     # fallback
                else:
                    msg = description

                # Run function
                try:
                    logger.log(level.upper(), f"[{action.upper()}]: {msg}")
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"[{action.upper()} FAILED] {msg} → {e}")
                    raise
            return wrapper
        return decorator
    return log_action
