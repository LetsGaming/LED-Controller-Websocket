import asyncio
import threading
import time
from flask import Blueprint, jsonify, request, make_response, Response, abort
from api.config import static_animations, standard_animations, custom_animations, special_animations
from utils.logger import LOGGER
from websocket.websocket_server import WebSocketServer

# Global Constants
LED_API_PORT = 8080
EXPECTED_WEBSOCKET_RESPONSES = {}

# Initialize WebSocketHandlerServer
websocket_server = None
websocket_handler = None

def websocket_server_callback(sid, response_data):
    """
    Callback function for WebSocket server.
    """
    # Check if sid is in the expected responses dictionary
    if sid in EXPECTED_WEBSOCKET_RESPONSES:
        current_response = EXPECTED_WEBSOCKET_RESPONSES[sid]
        current_response['response_data'] = response_data

def initialize_websocket_handler():
    global websocket_server, websocket_handler
    websocket_server = WebSocketServer(LED_API_PORT, websocket_server_callback)
    websocket_thread = threading.Thread(target=lambda: asyncio.run(websocket_server.init_server()))
    websocket_thread.start()
    websocket_handler = websocket_server.get_websocket_handler()

initialize_websocket_handler()

# Flask Blueprint
led_api = Blueprint('led_api', __name__)

# Utility Functions
def _add_expected_websocket_response(sid):
    EXPECTED_WEBSOCKET_RESPONSES[sid] = {'response_data': None}
    return EXPECTED_WEBSOCKET_RESPONSES[sid]

def _check_controller_id_exists(controller_id):
    if controller_id is None:
        abort(400, description='Controller ID is required.')

    connected_clients = websocket_server.get_connected_clients()

    if controller_id not in connected_clients:
        abort(404, description=f'Controller ID {controller_id} does not exist')

def _manipulate_response(flask_response: Response, response_data):
    flask_response.data = jsonify(message=response_data).get_data()
    flask_response.status_code = 200 if response_data.get('status') == 'success' else 500

async def _await_response_with_timeout(controller_id, timeout=15, check_interval=1, on_timeout_callback=None):
    awaited_response = _add_expected_websocket_response(controller_id)

    start_time = time.time()

    while not awaited_response['response_data']:
        if time.time() - start_time > timeout:
            if on_timeout_callback:
                on_timeout_callback(controller_id)
            return False

        await asyncio.sleep(check_interval)

    return True

async def _process_response(controller_id, flask_response):
    has_responded = await _await_response_with_timeout(controller_id)

    if has_responded:
        response_data = EXPECTED_WEBSOCKET_RESPONSES.get(controller_id)['response_data']
        _manipulate_response(flask_response, response_data)
    else:
        abort(400, description=f'Response timeout for Controller ID: {controller_id}. No response received.')

# General LED information endpoints
@led_api.route("/led/connected_controller", methods=['GET'])
def get_connected_controller():
    """
    Get the list of connected controllers.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    response = websocket_server.get_connected_clients()
    amount_of_clients = len(response)
    return (jsonify(message="Connected clients found", data=response), 200) if amount_of_clients > 0 else (jsonify(message="No connected clients"), 204)

# LED strip control endpoints
@led_api.route('/led/get_online_state/<int:controller_id>', methods=['GET'])
async def get_online_state(controller_id):
    _check_controller_id_exists(controller_id)
    await websocket_handler.get_online_state(controller_id)
    flask_response = make_response(jsonify(message="Request sent"), 200)
    await _process_response(controller_id, flask_response)
    return flask_response

@led_api.route('/led/set_online_state/<int:controller_id>', methods=['POST'])
async def set_online_state(controller_id):
    """
    Set the online state of the LED strip.

    Args:
        controller_id (int): Controller ID.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    _check_controller_id_exists(controller_id)
    data = request.get_json()
    value = data.get('online')
    await websocket_handler.set_online_state(controller_id, value)
    flask_response = make_response(jsonify(message="Command sent"), 200)
    await _process_response(controller_id, flask_response)
    return flask_response

@led_api.route('/led/get_brightness/<int:controller_id>', methods=['GET'])
async def get_brightness(controller_id):
    """
    Get the brightness of the LED strip.

    Args:
        controller_id (int): Controller ID.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    _check_controller_id_exists(controller_id)
    await websocket_handler.get_brightness(controller_id)
    flask_response = make_response(jsonify(message="Request sent"), 200)
    await _process_response(controller_id, flask_response)
    return flask_response

@led_api.route('/led/set_brightness/<int:controller_id>', methods=['POST'])
async def set_brightness(controller_id):
    """
    Set the brightness of the LED strip.

    Args:
        controller_id (int): Controller ID.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    _check_controller_id_exists(controller_id)
    data = request.get_json()
    brightness = data.get('brightness')
    await websocket_handler.set_brightness(controller_id, brightness)
    flask_response = make_response(jsonify(message="Command sent"), 200)
    await _process_response(controller_id, flask_response)
    return flask_response

@led_api.route('/led/all/<string:animation_name>', methods=['POST'])
async def start_animation_for_all(animation_name):
    """
    Start a certain animation for all connected clients.

    Args:
        animation_name (str): Name of the animation.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    option_mapping = {
        'set_online_state': websocket_handler.set_online_state,
        'set_brightness': websocket_handler.set_brightness
    }

    animation_mapping = {
        'static': static_animations,
        'standard': standard_animations,
        'custom': custom_animations,
        'special': special_animations
    }

    if animation_name.startswith("get"):
        return jsonify(message="Getting data from all controller at once, not yet implemented"), 501

    connected_clients = websocket_server.get_connected_clients()
    
    if not connected_clients:
        return jsonify(message="No clients connected."), 200
    
    if animation_name in option_mapping:
        func = option_mapping[animation_name]
        return await _start_func_for_all(func, connected_clients, request=request)

    animation_type = None
    for anim_type, anim_set in animation_mapping.items():
        if animation_name in anim_set:
            animation_type = anim_type
            break

    if not animation_type:
        return jsonify(message='Invalid animation name.'), 400

    start_animation_func = getattr(websocket_handler, f"start_{animation_type}_animation")
    if anim_type == "standard":
        return await _start_func_for_all(start_animation_func, connected_clients, animation_name=animation_name)
    return await _start_func_for_all(start_animation_func, connected_clients, animation_name, request)

async def _start_func_for_all(func, clients, animation_name=None, request=None):
    if not clients:
        return jsonify(message="No clients connected."), 200

    tasks = []
    for controller_id in clients:
        tasks.append(func(controller_id, animation_name, request.json))

    LOGGER.info(f"Data for all clients: func: {func} | clients: {clients} | animation_name: {animation_name} | request.json: {request.json}")
    await asyncio.gather(*tasks)
    return jsonify(message="Function called for all connected clients"), 200

# Animation endpoints
@led_api.route('/led/animation/static/<string:animation_name>/<int:controller_id>', methods=['POST'])
async def start_static_animation(controller_id, animation_name):
    """
    Start a custom animation on the LED strip.

    Args:
        controller_id (int): Controller ID.
        animation_name (str): Name of the custom animation.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    _check_controller_id_exists(controller_id)
    animation = static_animations.get(animation_name)
    if animation:
        args = animation['args']
        missing_args = [arg for arg in args if arg not in request.json]
        if missing_args:
            return jsonify(message=f'Missing arguments: {", ".join(missing_args)}'), 400

        await websocket_handler.start_static_animation(controller_id, animation_name, request.json)
        flask_response = make_response(jsonify(message="Command sent"), 200)
        await _process_response(controller_id, flask_response)
        return flask_response
    else:
        return jsonify(message='Invalid animation name.'), 400

@led_api.route('/led/animations/standard/<string:animation_name>/<int:controller_id>', methods=['POST'])
async def start_standard_animation(controller_id, animation_name):
    """
    Start a standard animation on the LED strip.

    Args:
        controller_id (int): Controller ID.
        animation_name (str): Name of the standard animation.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    _check_controller_id_exists(controller_id)
    animation = standard_animations.get(animation_name)
    if animation:
        await websocket_handler.start_standard_animation(controller_id, animation_name)
        flask_response = make_response(jsonify(message="Command sent"), 200)
        await _process_response(controller_id, flask_response)
        return flask_response
    else:
        return jsonify(message='Invalid animation name.'), 400

@led_api.route('/led/animations/custom/<string:animation_name>/<int:controller_id>', methods=['POST'])
async def start_custom_animation(controller_id, animation_name):
    """
    Start a custom animation on the LED strip.

    Args:
        controller_id (int): Controller ID.
        animation_name (str): Name of the custom animation.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    _check_controller_id_exists(controller_id)
    animation = custom_animations.get(animation_name)
    if animation:
        args = animation['args']
        missing_args = [arg for arg in args if arg not in request.json]
        if missing_args:
            return jsonify(message=f'Missing arguments: {", ".join(missing_args)}'), 400

        await websocket_handler.start_custom_animation(controller_id, animation_name, request.json)
        flask_response = make_response(jsonify(message="Command sent"), 200)
        await _process_response(controller_id, flask_response)
        return flask_response
    else:
        return jsonify(message='Invalid animation name.'), 400

@led_api.route('/led/animations/special/<string:animation_name>/<int:controller_id>', methods=['POST'])
async def start_special_animation(controller_id, animation_name):
    """
    Start a special animation on the LED strip.

    Args:
        controller_id (int): Controller ID.
        animation_name (str): Name of the special animation.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    _check_controller_id_exists(controller_id)
    animation = special_animations.get(animation_name)
    if animation:
        args = animation['args']
        missing_args = [arg for arg in args if arg not in request.json]
        if missing_args:
            return jsonify(message=f'Missing arguments: {", ".join(missing_args)}'), 400

        await websocket_handler.start_special_animation(controller_id, animation_name, request.json)
        flask_response = make_response(jsonify(message="Command sent"), 200)
        await _process_response(controller_id, flask_response)
        return flask_response
    else:
        return jsonify(message='Invalid animation name.'), 400

# Animation information endpoints
@led_api.route('/led/animations/static', methods=['GET'])
def get_static_animations():
    """
    Get the list of start animations.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    return jsonify(static_animations), 200

@led_api.route('/led/animations/standard', methods=['GET'])
def get_standard_animations():
    """
    Get the list of standard animations.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    return jsonify(standard_animations), 200

@led_api.route('/led/animations/custom', methods=['GET'])
def get_custom_animations():
    """
    Get the list of custom animations.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    return jsonify(custom_animations), 200

@led_api.route('/led/animations/special', methods=['GET'])
def get_special_animations():
    """
    Get the list of special animations.

    Returns:
        tuple: Tuple containing JSON response and HTTP status code.
    """
    return jsonify(special_animations), 200
