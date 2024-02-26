import logging
from logging.handlers import RotatingFileHandler
import os

def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Log to console
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Ensure the 'logs' folder exists, create it if not
    logs_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(logs_folder, exist_ok=True)

    # Log to a rotating file (info.log) for INFO level logs
    log_file_path = os.path.join(logs_folder, 'info.log')
    fh_info = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)  # 10 MB per file, keep 5 backups
    fh_info.setLevel(logging.INFO)  # Set the handler to handle INFO level logs
    fh_info.setFormatter(formatter)
    logger.addHandler(fh_info)

    # Log errors to a separate file (error.log)
    error_log_file_path = os.path.join(logs_folder, 'error.log')
    fh_error = RotatingFileHandler(error_log_file_path, maxBytes=10*1024*1024, backupCount=5)
    fh_error.setLevel(logging.ERROR)
    fh_error.setFormatter(formatter)
    logger.addHandler(fh_error)

    return logger

LOGGER = init_logger()
