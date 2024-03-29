import os
import json
import asyncio 
import logging
import argparse
from led.controller import LEDController
from websocket.websocket_handler import WebSocketHandlerClient

def _init_logger():
    logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create a logger instance
    return logging.getLogger(__name__)

def load_config():
    """
    Load configuration from the 'config.json' file located in the same directory as this script.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")

    with open(config_path, 'r') as file:
        return json.load(file)

async def main(name=None):
    """
    Main function to initialize and run the LED controller and WebSocket handler.
    """
    config = load_config()
    LOGGER = _init_logger()

    strip_config = config["strip"]
    led_controller = LEDController(LOGGER, strip_config)
    wbs_handler = WebSocketHandlerClient(name, config["websocket"]["server_address"], config["websocket"]["server_port"], led_controller, LOGGER)
    await wbs_handler.connect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LED Controller with WebSocket Handler")
    parser.add_argument("--name", help="Specify a name for the WebSocket handler")

    args = parser.parse_args()

    # Create an event loop and run the main coroutine, passing the 'name' argument
    asyncio.run(main(name=args.name))
