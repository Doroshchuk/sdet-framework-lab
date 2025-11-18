from common.utils.log_action import make_log_action, LogActionType
from sauce_demo_ui.utils.logger import logger


log_step = make_log_action(logger, LogActionType.STEP)
log_flow = make_log_action(logger, LogActionType.FLOW)