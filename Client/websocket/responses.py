from enum import Enum
from utils.logger import LOGGER

class BaseResponse(Enum):
    """
    Base class for error and success responses
    """
    def __init__(self, status, message, data=None):
        self._status = status
        self._message = message
        self._data = data

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self._message

    @property
    def data(self):
        return self._data

class Errors(Enum):
    """
    Enums for error responses
    """
    GENERAL_ERROR = ('error', 'Something went wrong')
    UNKNOWN_COMMAND = ('error', 'Unknown command')
    UNKNOWN_REQUEST = ('error', 'Unknown request')
    UNKNOWN_ANIMATION = ('error', 'Unknown animation')
    MISSING_ARGUMENT = ('error', 'Missing argument')

class Successes(Enum):
    """
    Enums for success responses
    """
    REQUEST_SUCCESS = ('success', 'request completed')
    COMMAND_SUCCESS = ('success', 'command completed')

class ResponseFactory:
    """
    Class for response factory
    """
    
    @staticmethod
    def create_error_response(error_type: Errors, data=None) -> dict:
        """
        Factory function to create an error response
        """
        response = {
            'status': error_type.value[0],
            'message': error_type.value[1],
        }
        if data:
            response['data'] = data
        return response

    @staticmethod
    def create_success_response(success_type: Successes, data=None) -> dict:
        """
        Factory function to create a success response
        """
        response = {
            'status': success_type.value[0],
            'message': success_type.value[1]
        }
        if data:
            response['data'] = data
        return response

class CommandResponses(ResponseFactory):
    """
    Class for command responses
    """

class RequestResponses(ResponseFactory):
    """
    Class for request responses
    """