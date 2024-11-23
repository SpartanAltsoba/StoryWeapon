# logger.py

import logging
from logging.handlers import RotatingFileHandler
import os
from config import Config

# Ensure the logs directory exists
logs_dir = os.path.dirname(Config.LOG_FILE)
os.makedirs(logs_dir, exist_ok=True)

# Create a rotating file handler
file_handler = RotatingFileHandler(
    Config.LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=5
)

# Define logging format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
file_handler.setFormatter(formatter)

# Get the global logger
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)

# Prevent adding multiple handlers to the logger
if not logger.handlers:
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
