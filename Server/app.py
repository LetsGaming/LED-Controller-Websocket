from flask import Flask, send_file
from flask_cors import CORS
import importlib
import os
from utils.logger import LOGGER
from utils.utils import ROOT_DIR, load_config

_api_config = None

def load_api_config():
    config = load_config()
    _api_config = config.get("api", {})

    return _api_config

def load_allowed_origins():
    return _api_config.get("allowed_origins", [])

def load_port():
    port = _api_config.get("port", 5000)
    try:
        return int(port)
    except (TypeError, ValueError):
        LOGGER.warning(f"Invalid port in config.json, defaulting to 5000.")
        return 5000

def create_app():
    app = Flask(__name__)
    load_api_config()

    # Read allowed origins from config.json
    allowed_origins = load_allowed_origins()
    CORS(app, origins=allowed_origins)

    # Dynamically import and register API blueprints
    api_directory = "api"
    not_allowed_names = ["__init__.py", "config.py"]

    api_path = os.path.join(ROOT_DIR, api_directory)
    api_files = [
        file[:-3]
        for file in os.listdir(api_path)
        if file.endswith(".py") and file not in not_allowed_names
    ]

    for api_file in api_files:
        module = importlib.import_module(f"{api_directory}.{api_file}")
        blueprint = getattr(module, f"{api_file}_api")
        app.register_blueprint(blueprint)

    return app

app = create_app()

@app.route("/favicon.ico", methods=["GET"])
def favicon():
    """Handle the request for the favicon.ico file."""
    return send_file(
        path_or_file=os.path.join(ROOT_DIR, "favicon.ico"),
        mimetype="image/vnd.microsoft.icon",
    )

if __name__ == "__main__":
    try:
        port = load_port()
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
