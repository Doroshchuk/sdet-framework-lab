from common.utils.log_action import make_log_action, ActionType
from sauce_demo_ui.utils.logger import logger


log_step = make_log_action(logger, ActionType.STEP)
log_flow = make_log_action(logger, ActionType.FLOW)