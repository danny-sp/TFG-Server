import logging
import os
import sys
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger instance with a specific format.
    Logs to both console and file.
    """
    # Create a custom logger
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers if the logger already exists (Singleton-like behavior)
    if logger.hasHandlers():
        return logger

    # Set the threshold of logger to level defined in .env
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(log_level)

    # Create formatters
    # Format: [Time] [Logger Name] [Line] [Level]: Message
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(lineno)d - %(levelname)s: %(message)s')

    # Create console handler
    c_handler = logging.StreamHandler(sys.stdout)
    c_handler.setLevel(log_level)
    c_handler.setFormatter(log_format)

    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create file handler with timestamp in filename
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(log_dir, f'{timestamp}.log')
    f_handler = logging.FileHandler(log_file, encoding='utf-8')
    f_handler.setLevel(log_level)
    f_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger