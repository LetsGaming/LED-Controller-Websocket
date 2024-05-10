from websocket.commands import Command, CommandType, RequestType

class WebSocketCommandHandler:
    def __init__(self, send_message):
        self.send_message = send_message
        
    async def _send_command(self, sid, command_type, rgb_data=None, animation_data=None):
        command = Command(command_type, rgb_data, animation_data)
        await self.send_message(sid, command.to_dict())

    async def get_online_state(self, sid):
        await self._send_command(sid, RequestType.GET_ONLINE_STATE)

    async def get_brightness(self, sid):
        await self._send_command(sid, RequestType.GET_BRIGHTNESS)

    async def set_online_state(self, sid, value):
        await self._send_command(sid, CommandType.SET_ONLINE_STATE, animation_data={'value': value})

    async def set_brightness(self, sid, brightness):
        await self._send_command(sid, CommandType.SET_BRIGHTNESS, animation_data={'brightness': brightness})

    async def start_static_animation(self, sid, animation_name, request_data):
        await self._send_command(sid, CommandType.START_START_ANIMATION, animation_data={'animation_name': animation_name, 'args': request_data})
    
    async def start_standard_animation(self, sid, animation_name):
        await self._send_command(sid, CommandType.START_STANDARD_ANIMATION, animation_data={'animation_name': animation_name})

    async def start_custom_animation(self, sid, animation_name, request_data):
        await self._send_command(sid, CommandType.START_CUSTOM_ANIMATION, animation_data={'animation_name': animation_name, 'args': request_data})

    async def start_special_animation(self, sid, animation_name, request_data):
        await self._send_command(sid, CommandType.START_SPECIAL_ANIMATION, animation_data={'animation_name': animation_name, 'args': request_data})
