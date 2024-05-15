from enum import Enum

from utils.logger import LOGGER

class BaseResponse(Enum):
    """
    Base class for error and success responses
    """
    def __init__(self, status, message, data=None):
        self.status = status
        self.message = message
        self.data = data

class Errors(BaseResponse):
    """
    Enums for error responses
    """
    GENERAL_ERROR = ('error', 'Something went wrong')
    UNKNOWN_COMMAND = ('error', 'Unknown command')
    UNKNOWN_REQUEST = ('error', 'Unknown request')
    UNKNOWN_ANIMATION = ('error', 'Unknown animation')
    MISSING_ARGUMENT = ('error', 'Missing argument')

class Successes(BaseResponse):
    """
    Enums for success responses
    """
    REQUEST_SUCCESS = ('success', 'request completed')
    COMMAND_SUCCESS = ('success', 'command completed')

class ResponseFactory:
    """
    Class for response factory
    """
    def create_error_response(self, error_type: Errors, **kwargs) -> dict:
        """
        Factory function to create an error response
        """
        LOGGER.info(f"Error_type: {error_type}")
        LOGGER.info(f"kwargs: {kwargs}")
        response = error_type.value._asdict()
        for key, value in kwargs.items():
            response[key] = value
        return response

    def create_success_response(self, success_type: Successes, data=None) -> dict:
        """
        Factory function to create a success response
        """
        LOGGER.info(f"Success_type: {success_type}")
        response = success_type.value._asdict()
        response['data'] = data
        return response

class CommandResponses(ResponseFactory):
    """
    Class for command responses
    """
    def __init__(self):
        super().__init__()

class RequestResponses(ResponseFactory):
    """
    Class for request responses
    """
    def __init__(self):
        super().__init__()