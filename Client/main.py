import os
import json
import asyncio
import argparse
from led.controller import LEDController
from websocket.websocket_handler import WebSocketHandlerClient

from utils.logger import LOGGER

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
    try:
        config = load_config()

        strip_config = config["strip"]
        sunset_config = config["sunset_provider"]
        led_controller = LEDController(strip_config, sunset_config)
        
        wbs_config = config["websocket"]
        wbs_handler = WebSocketHandlerClient(name, wbs_config["server_address"], wbs_config["server_port"], led_controller)
        await wbs_handler.connect()
    except Exception as e:
        LOGGER.error(f"Error: {e}")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LED Controller with WebSocket Handler")
    parser.add_argument("--name", help="Specify a name for the WebSocket handler")

    args = parser.parse_args()

    # Create an event loop and run the main coroutine, passing the 'name' argument
    asyncio.run(main(name=args.name))
