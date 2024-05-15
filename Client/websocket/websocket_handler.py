import asyncio
import json
import os
import websockets
from logging import Logger
from led.controller import LEDController, OFFLINE_ERROR

from websocket.responses import *

SAVE_PATH =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'saved_animation.json')

class WebSocketHandlerClient:
    """
    Handles WebSocket communication for the LED controller client.
    """

    def __init__(self, client_name: str, server_address: str, server_port: str, led_controller: LEDController, logger: Logger,):
        """
        Initializes the WebSocketHandlerClient.

        Args:
            client_name (str): The name the client should conenct with.
            server_address (str): The address of the WebSocket server.
            server_port (str): The port of the WebSocket server.
            led_controller (LEDController): An instance of the LEDController.
            logger (Logger): Logger to log messages and other information.
        """
        self.client_name = client_name
        self.server_address = server_address
        self.server_port = server_port
        self.led_controller = led_controller
        self.logger = logger
        
        # Map command names to handler methods
        self.handlers = {
            'set_online_state': self.led_controller.set_online_state,
            'set_brightness': self.led_controller.set_brightness,
            'start_static_animation': self.start_static_animation,
            'start_standard_animation': self.start_standard_animation,
            'start_custom_animation': self.start_custom_animation,
            'start_special_animation': self.start_special_animation
        }

        # Map standard animation names to methods
        self.static_animations = {
            'white': self.led_controller.set_white,
            'custom_color': self.led_controller.fill_color,
            'custom_fill': self.led_controller.custom_fill,
        }
        
        self.standard_animations = {
            'rainbow_cycle': self.led_controller.rainbow_cycle,
            'rainbow_comet': self.led_controller.rainbow_comet,
            'theater_chase_rainbow': self.led_controller.theater_chase_rainbow,
            'rainbow_bounce': self.led_controller.rainbow_bounce,
            'random_bounce': self.led_controller.random_bounce
        }

        # Map custom and special animation names to methods
        self.custom_animations = {
            'color_wipe': self.led_controller.color_wipe,
            'theater_chase': self.led_controller.theater_chase,
            'strobe': self.led_controller.strobe,
            'color_chase': self.led_controller.color_chase,
            'custom_rainbow_cycle': self.led_controller.custom_rainbow_cycle,
        }
        
        self.special_animations = {
            'blink': self.led_controller.blink,
            'fade': self.led_controller.fade,
            'sparkle': self.led_controller.sparkle,
            'scanner_effect': self.led_controller.scanner_effect,
            'yoyo_theater': self.led_controller.yoyo_theater,
            'breathing_effect': self.led_controller.breathing_effect,
            'color_ripple': self.led_controller.color_ripple,
        }
        
        self._load_animation_from_file()
        
    async def connect(self):
        """
        Establishes a WebSocket connection to the server.
        """
        while True:
            try:
                uri = f"ws://{self.server_address}:{self.server_port}"
                async with websockets.connect(uri, ping_interval=None) as websocket:
                    self.websocket = websocket
                    self.logger.info(f"Connected to WebSocket server at {self.server_address}")
                    await self.send_message({'name': self.client_name})
                    await self.handle_messages()
            except Exception as e:
                self.logger.error(f"Failed to connect to WebSocket server. Error: {e}")
                await asyncio.sleep(5) 

    async def send_message(self, message: dict):
        """
        Sends a JSON-formatted message to the WebSocket server.

        Args:
            message (dict): The message to be sent.
        """
        try:
            await self.websocket.send(json.dumps(message))
            self.logger.info(f"Sent message to server: {message}")
        except Exception as e:
            self.logger.error(f"Failed to send message to server: {message}. Error: {e}")

    async def handle_messages(self):
        """
        Continuously handles incoming messages from the WebSocket server.
        """
        while True:
            try:
                message = await self.websocket.recv()
                await self.handle_message(message)
                await asyncio.sleep(.1)
            except websockets.exceptions.ConnectionClosed:
                self.logger.warning("WebSocket connection closed unexpectedly. Reconnecting...")
                await self.connect()

    async def handle_message(self, message):
        """
        Processes a received message from the WebSocket server.

        Args:
            message (str): The received message.
        """
        try:
            data = json.loads(message)
            self.logger.info(f"Message recieved from server: {data}")
            event = data.get('event')
            if event == 'command':
                await self.handle_command(data)
            elif event == 'request':
                await self.handle_request(data)
        except json.JSONDecodeError:
            self.logger.error(f"Failed to decode JSON message: {message}")

    async def handle_request(self, request_data):
        """
        Handles incoming requests from the server.

        Args:
            request_data (dict): The request data received from the server.
        """
        request_name = request_data.get('request_name')
        if not request_name:
            response = RequestResponses.create_error_response(Errors.MISSING_ARGUMENT, 'request_name')
            await self.send_message(response)
        else:
            response = self.dispatch_request(request_name)
            await self.send_message(response)

    async def handle_command(self, command_data):
        """
        Handles incoming commands from the server.

        Args:
            command_data (dict): The command data received from the server.
        """
        # Check if the command has the required keys
        command_name = command_data.get('command_name')
        args = command_data.get('data')

        if not command_name:
            response = CommandResponses.create_error_response(Errors.MISSING_ARGUMENT, "command_name")
        else:
            # Dispatch the command to the appropriate handler
            response = self.dispatch_command(command_name, args)

        await self.send_message(response)

    def dispatch_request(self, request_name):
        """
        Dispatches a request to the LED controller.

        Args:
            request_name (str): The name of the request.

        Returns:
            dict: The response from the LED controller.
        """
        handlers = {
            'get_online_state': self.led_controller.get_online_state,
            'get_brightness': self.led_controller.get_brightness
        }

        # Check if the request name is valid
        if request_name not in handlers:
            self.logger.error('Unknown request: %s', request_name)
            return RequestResponses.create_error_response(Errors.UNKNOWN_REQUEST)

        # Call the appropriate handler and return its response
        strip_response = handlers[request_name]()
        if strip_response == OFFLINE_ERROR:
            self.logger.error('Error: %s', strip_response)
            return RequestResponses.create_error_response(Errors.GENERAL_ERROR, strip_response)
        else:
            self.logger.info('Request completed successfully')
            return RequestResponses.create_success_response(Successes.REQUEST_SUCCESS, strip_response)

    def dispatch_command(self, command_name, args):
        """
        Dispatches a command to the LED controller.

        Args:
            command_name (str): The name of the command.
            args (dict): Arguments for the command.

        Returns:
            dict: The response from the LED controller.
        """
        # Check if the command name is valid
        if command_name not in self.handlers:
            self.logger.error('Unknown command: %s', command_name)
            return CommandResponses.create_error_response(Errors.UNKNOWN_COMMAND)

        # Call the appropriate handler and return its response
        strip_response = self.handlers[command_name](**args)
        if strip_response == OFFLINE_ERROR:
            self.logger.error('Error: %s', strip_response)
            return CommandResponses.create_error_response(Errors.GENERAL_ERROR, strip_response)
        else:
            self.logger.info('Request completed successfully')
            return CommandResponses.create_success_response(Successes.REQUEST_SUCCESS, strip_response)
    
    def _check_animation_name(self, name, animations):
        if not name:
            self.logger.error('No animation name provided')
            return CommandResponses.create_error_response(Errors.MISSING_ARGUMENT, 'animation_name')
        
        if name not in animations:
            self.logger.error('Unknown animation: %s', name)
            return CommandResponses.create_error_response(Errors.UNKNOWN_ANIMATION)
    
    def start_static_animation(self, **data):
        animation_name = data['animation_name']
        args = data['args']
        self._check_animation_name(animation_name, self.static_animations)

        self._save_animation_to_file(data, 'start')
        return self.static_animations[animation_name](**args)
    
    def start_standard_animation(self, animation_name):
        self._check_animation_name(animation_name, self.standard_animations)
        
        self._save_animation_to_file({'animation_name': animation_name}, 'standard')
        return self.standard_animations[animation_name]()

    def start_custom_animation(self, **data):
        animation_name = data['animation_name']
        args = data['args']
        self._check_animation_name(animation_name, self.custom_animations)
        
        self._save_animation_to_file(data, 'custom')
        return self.custom_animations[animation_name](**args)

    def start_special_animation(self, **data):
        animation_name = data['animation_name']
        args = data['args']
        self._check_animation_name(animation_name, self.special_animations)
        
        self._save_animation_to_file(data, 'special')
        return self.special_animations[animation_name](**args)
        
    def _save_animation_to_file(self, animation_data: dict, type: str):
        self.logger.info("Saving animation to json")
        data = animation_data
        data['type'] = type
        data['brightness'] = self.led_controller.get_brightness()
        with open(SAVE_PATH, 'w') as f:
            json.dump(data, f, indent=4)
            
    def _load_animation_from_file(self):
        try:
            with open(SAVE_PATH, 'r') as f:
                data = json.load(f)
                if not data:
                    return
                
                self.__handle_loaded_data(data)
                    
        except FileNotFoundError:
            pass
    
    def __handle_loaded_data(self, data):
        self.led_controller.set_online_state(True)
                
        animation_type = data['type']
        if not animation_type:
            self.logger.error('Missing animation type when handling loaded data')
        del data['type']
        
        self.led_controller.set_brightness(data['brightness'])
        del data['brightness']
        
        self.logger.info('Starting animation: %s', animation_type)
        if animation_type == 'standard':
            animation_name = data['animation_name']
            self.start_standard_animation(animation_name)
        elif animation_type == 'custom':
            self.start_custom_animation(**data)
        elif animation_type == 'special':
            self.start_special_animation(**data)