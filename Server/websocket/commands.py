from enum import Enum
from typing import Union

class RGBValues():
    """
    Represents RGB color values with attributes for red, green, and blue.
    """

    def __init__(self, red: int, green: int, blue: int):
        """
        Initializes RGBValues with specified red, green, and blue values.

        Args:
            red (int): Red color value (0-255).
            green (int): Green color value (0-255).
            blue (int): Blue color value (0-255).
        """
        self.red = red
        self.green = green
        self.blue = blue
        self._init_data()

    def _init_data(self):
        """
        Initializes the data attribute with a dictionary containing RGB values.
        """
        self.data = {
            _RGBData.RED.value: self.red,
            _RGBData.GREEN.value: self.green,
            _RGBData.BLUE.value: self.blue,
        }

class _RGBData(Enum):
    """
    Enum representing RGB color channels.
    """
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

class CommandType(Enum):
    """
    Enum representing different command types for controlling the websocket LED-Strips.
    """
    SET_ONLINE_STATE = 'set_online_state'
    SET_BRIGHTNESS = 'set_brightness'
    
    START_START_ANIMATION = 'start_start_animation'
    START_STANDARD_ANIMATION = 'start_standard_animation'
    START_CUSTOM_ANIMATION = 'start_custom_animation'
    START_SPECIAL_ANIMATION = 'start_special_animation'

class RequestType(Enum):
    """
    Enum representing different request types for querying LED-Strips information.
    """
    GET_ONLINE_STATE = 'get_online_state'
    GET_BRIGHTNESS = 'get_brightness'


class Command:
    """
    Represents a command to control LED strips or request information.
    """

    def __init__(self, type: Union[RequestType, CommandType], rgb_data: RGBValues, animation_data):
        """
        Initializes a Command instance with the specified type, RGB data, and animation data.

        Args:
            type (Union[RequestType, CommandType]): Type of the command (request or control).
            rgb_data (RGBValues): RGB color data associated with the command.
            animation_data: Additional animation data for the command.
        """
        if not isinstance(type, (RequestType, CommandType)):
            raise ValueError("Invalid request type. Must be of type RequestType or CommandType.")

        self.type = type
        self.rgb_data = rgb_data
        self.animation_data = animation_data
        self._init_data()

    def _init_data(self):
        """
        Initializes the data attribute with a combined dictionary of RGB and animation data.
        """
        self.data = {} 
        if self.rgb_data and self.animation_data:
            self.data = {**self.rgb_data.data, **self.animation_data}
        elif self.rgb_data:
            self.data.update(self.rgb_data.data)
        elif self.animation_data:
            self.data = self.animation_data
            
    def to_dict(self):
        """
        Converts the Command instance to a dictionary format.

        Returns:
            dict: Dictionary representation of the command.
        """
        event_type = 'command' if isinstance(self.type, CommandType) else 'request'
        type_name = 'command_name' if isinstance(self.type, CommandType) else 'request_name'
        
        return {'event': event_type, type_name: self.type.value, 'data': self.data}
