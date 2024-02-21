import json
import websockets
from websockets.server import serve
from logging import Logger
import asyncio
from websocket.commands import Command, CommandType, RequestType, RGBValues

class WebSocketHandlerServer:
    def __init__(self, logger: Logger, port: int, callback):
        self.connected_clients = {}
        self.server = None
        self.port = port
        self.callback = callback

        self.logger = logger

    async def init_handler(self):
        host = ''
        async with serve(self.handle_connection, host, self.port, ping_interval=None) as server:
            self.server = server
            self.logger.info(f"WebSocket server started at {'all possible interfaces' if host == '' else f'ws://{host}:{self.port}'}")
            await asyncio.Future()

    def get_connected_clients(self):
        return self.connected_clients

    async def handle_connection(self, websocket):
        sid = id(websocket)
        self.connected_clients[sid] = {'id': sid, 'name': 'none'} 
        self.logger.info(f"Client {sid} connected")

        try:
            # Receive the initial message for setting the name
            initial_message = await websocket.recv()
            name_data = json.loads(initial_message)
            client_name = name_data.get('name')

            if client_name:
                self.connected_clients[sid]['name'] = client_name

            async for message in websocket:
                data = json.loads(message)
                self.logger.info(f"Message from client {sid}: {data}")
                await self.handle_response(sid, data)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.handle_disconnection(sid)

    async def handle_disconnection(self, sid):
        if sid in self.connected_clients:
            client_name = self.connected_clients[sid]['name']
            del self.connected_clients[sid]
            self.logger.info(f"Client {client_name} ({sid}) disconnected")

    def _add_client(self, client_name, sid):
        next_index = len(self.connected_clients)
        if client_name:
            self.connected_clients[next_index] = {'id': sid, 'name': client_name}
        else:
            self.connected_clients[next_index] = {'id': sid, 'name': 'none'}
            
    async def _send_message_to_client(self, sid, data):
        websocket = next((ws for ws in self.server.websockets if id(ws) == sid), None)
        if websocket:
            await websocket.send(json.dumps(data))

    async def handle_response(self, sid, data):
        self.callback(sid, data)

    async def _send_command(self, sid, command_type, rgb_data=None, animation_data=None):
        command = Command(command_type, rgb_data, animation_data)
        await self._send_message_to_client(sid, command.to_dict())

    async def get_online_state(self, sid):
        await self._send_command(sid, RequestType.GET_ONLINE_STATE)

    async def get_brightness(self, sid):
        await self._send_command(sid, RequestType.GET_BRIGHTNESS)

    async def set_online_state(self, sid, value):
        await self._send_command(sid, CommandType.SET_ONLINE_STATE, animation_data={'value': value})

    async def set_brightness(self, sid, brightness):
        await self._send_command(sid, CommandType.SET_BRIGHTNESS, animation_data={'brightness': brightness})

    async def set_white(self, sid):
        await self._send_command(sid, CommandType.SET_WHITE)

    async def fill_color(self, sid, red, green, blue):
        await self._send_command(sid, CommandType.FILL_COLOR, rgb_data=RGBValues(red, green, blue))

    async def custom_fill(self, sid, red, green, blue, percentage):
        await self._send_command(sid, CommandType.CUSTOM_FILL, rgb_data=RGBValues(red, green, blue), animation_data={'percentage': percentage})

    async def start_standard_animation(self, sid, animation_name):
        await self._send_command(sid, CommandType.START_STANDARD_ANIMATION, animation_data={'animation_name': animation_name})

    async def start_custom_animation(self, sid, animation_name, request_data):
        await self._send_command(sid, CommandType.START_CUSTOM_ANIMATION, animation_data={'animation_name': animation_name, 'args': request_data})

    async def start_special_animation(self, sid, animation_name, request_data):
        await self._send_command(sid, CommandType.START_SPECIAL_ANIMATION, animation_data={'animation_name': animation_name, 'args': request_data})
