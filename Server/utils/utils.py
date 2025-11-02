import os
import json
from utils.logger import LOGGER

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_config = None  # internal cache

def load_config():
    """
    Loads and caches the configuration from config.json.
    Returns an empty dict if not found or invalid.
    """
    global _config
    if _config is not None:
        return _config

    config_path = os.path.join(ROOT_DIR, "config.json")

    try:
        with open(config_path, "r") as config_file:
            _config = json.load(config_file)
            return _config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        LOGGER.warning(f"Could not load config.json: {e}")
        _config = {}
        return _config
