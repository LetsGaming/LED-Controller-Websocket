import json
import websockets
from websockets.server import serve
import asyncio
from utils.logger import LOGGER
from websocket.websocket_command_handler import WebSocketCommandHandler

class WebSocketServer:
    def __init__(self, port: int, callback, allow_duplicate_client_names = False):
        self.connected_clients = {}
        self.server = None
        self.handler = WebSocketCommandHandler(self.send_message)
        self.port = port
        self.callback = callback
        self.allow_duplicate_client_names = allow_duplicate_client_names

    async def init_server(self):
        host = '0.0.0.0'
        try:
            async with serve(self.__handle_connection, host, self.port, ping_interval=None) as server:
                self.server = server
                LOGGER.info(f"WebSocket server started at {f'all possible interfaces and port {self.port}' if host == '0.0.0.0' else f'ws://{host}:{self.port}'}")
                await asyncio.Future()
        except Exception as e:
            LOGGER.error(f"WebSocket server initialization error: {e}")

    async def __handle_connection(self, websocket, path):
        sid = id(websocket)
        client_name = None

        self.connected_clients[sid] = {'id': sid, 'name': client_name} 
        LOGGER.info(f"Client {sid} connected")

        try:
            # Receive the initial message for setting the name
            initial_message = await websocket.recv()
            name_data = json.loads(initial_message)
            client_name = name_data.get('name')

            if client_name:
                if not self.allow_duplicate_client_names:
                    await self.__disconnect_duplicate_client(client_name)
                self.connected_clients[sid]['name'] = client_name

            async for message in websocket:
                data = json.loads(message)
                LOGGER.info(f"Message from client {sid}: {data}")
                await self.handle_response(sid, data)
        except websockets.exceptions.ConnectionClosed:
            await self.__handle_disconnection(sid)
        finally:
            await self.__handle_disconnection(sid)

    async def __disconnect_duplicate_client(self, client_name: str):
        # Check if a client with the same name already exists
        for client in self.connected_clients.values():
            if client['name'] == client_name:
                await self.__handle_disconnection(client['id'])
                break
    
    async def __handle_disconnection(self, sid):
        client_data = self.connected_clients.pop(sid, None)
        if client_data:
            client_name = client_data['name']
            
            websocket = next((ws for ws in self.server.websockets if id(ws) == sid), None)
            if websocket:
                await websocket.close()
                
            LOGGER.info(f"Client {client_name} ({sid}) disconnected")

    async def handle_response(self, sid, data):
        self.callback(sid, data)

    async def _send_message_to_client(self, sid, data):
        websocket = next((ws for ws in self.server.websockets if id(ws) == sid), None)
        if websocket:
            await websocket.send(json.dumps(data))

    async def send_message(self, sid, data):
        await self._send_message_to_client(sid, data)

    def get_websocket_handler(self):
        return self.handler

    def get_connected_clients(self):
        return self.connected_clients