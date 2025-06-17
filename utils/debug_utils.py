from utils.config import config
import logging
import traceback

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def log_error_with_traceback(error_message: str) -> None:
    """
    Log an error message along with its traceback for debugging purposes.
    """
    logger.error(f"Error: {error_message}")
    logger.error("Stack Trace:")
    logger.error(traceback.format_exc())

def enable_debugging_mode() -> None:
    """
    Enables detailed logging for debugging purposes.
    """
    logging.getLogger().setLevel(logging.DEBUG)
    logger.info("Debugging mode enabled.")

def disable_debugging_mode() -> None:
    """
    Disables detailed debugging logs and reverts to normal logging.
    """
    logging.getLogger().setLevel(logging.INFO)
    logger.info("Debugging mode disabled.")