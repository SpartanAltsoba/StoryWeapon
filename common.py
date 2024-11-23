# common.py

import logging
from functools import wraps
import os

class CustomLogger:
    @staticmethod
    def get_logger(name, log_file=None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # If a log file is not provided, use the default from Config
        if not log_file:
            from config import Config
            log_file = Config.LOG_FILE

        # Check if handlers already exist to prevent duplicate logs
        if not logger.handlers:
            # Create handlers
            c_handler = logging.StreamHandler()
            f_handler = logging.FileHandler(log_file)
            c_handler.setLevel(logging.DEBUG)
            f_handler.setLevel(logging.DEBUG)

            # Create formatters and add to handlers
            c_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
            )
            f_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
            )
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)

            # Add handlers to the logger
            logger.addHandler(c_handler)
            logger.addHandler(f_handler)

        return logger

def log_function(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"Entering function: {func.__name__}")
            result = func(*args, **kwargs)
            logger.debug(f"Exiting function: {func.__name__}")
            return result
        return wrapper
    return decorator
