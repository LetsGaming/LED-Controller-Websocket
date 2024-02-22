# LED Controller GitHub Repository
Welcome to the LED Controller repository!<br>
This project enables you to control a LED strip connected to a Raspberry Pi GPIO using a Python Flask API, WebSocket server, and an Ionic Vue-based GUI.

## Important
* This implementation is only meant for local deployment! 
* There are basically no security checks added, so there is no rate-limiting or much input validation or anything else!!
    - If you want to add those implementations, feel free to create a fork of this repository.

## Features
### Server:
* Python Flask API for handling API requests.
* WebSocket server for real-time communication.
### GUI (Ionic Vue):
* User-friendly interface for controlling the LED strip.
* Interacts with the server through the API and WebSocket.
### Client (Raspberry Pi):
* Connects to the WebSocket server.
* Controls the LED strip through GPIO pins.

## Requirements
* Python 3.x
* Flask
* Raspberry Pi with GPIO pins
* Ionic Vue

## Installation
1. Clone the repository:
 
```bash 
git clone https://github.com/LetsGaming/LED-Controller-Websocket.git
cd LED-Controller
```
2. Install the required dependencies:

```bash 
pip install -r Client/requirements.txt
pip install -r Server/requirements.txt
```

3. For the GUI, follow the installation instructions for Ionic Vue on their official website.
* [Ionic-Website](https://ionicframework.com/docs/intro/cli)

## Usage
1. Start the Server:
```bash
cd server
python app.py
```
This will start the Flask API and WebSocket server.

2. Launch the GUI:
```bash
cd gui
ionic serve
```
Access the GUI through your web browser at http://localhost:8100.

Run the Client on Raspberry Pi:
```bash
cd client
python client.py --name NAME_OF_THE_CONTROLLER_TO_BE_SHOWN
```
Ensure that the Raspberry Pi is connected to the LED strip via GPIO pins set in the config.json.<br>
Now you can control the LED strip using the GUI and observe real-time updates!

## Contributing
We welcome contributions! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

## License
This project is licensed under the [MIT License](LICENSE.md). Feel free to use, modify, and distribute it as per the terms of the license.





