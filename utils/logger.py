from utils.config import config
# utils/logging/logger.py

import logging
from typing import Callable

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Use logging.info directly for log_event
log_event: Callable[[str], None] = logging.info

# Now, log_event is just an alias for logging.info and matches the expected type