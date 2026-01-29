import logging
import os
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger instance with a specific format.
    """
    # Create a custom logger
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers if the logger already exists (Singleton-like behavior)
    if logger.hasHandlers():
        return logger

    # Set the threshold of logger to level defined in .env
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(log_level)

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    c_handler.setLevel(log_level)

    # Create formatters and add it to handlers
    # Format: [Time] [Logger Name] [Level]: Message
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)

    return logger