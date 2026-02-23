from common.utils.log_action import make_log_action, LogActionType, LogLevelType
from sauce_demo_ui.framework.logging.logger import logger


log_step = make_log_action(logger, LogActionType.STEP)
log_flow = make_log_action(logger, LogActionType.FLOW)

__all__ = ["log_step", "log_flow", "LogActionType", "LogLevelType"]