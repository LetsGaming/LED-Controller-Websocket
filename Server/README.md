
# Server Component - Flask API and WebSocket Server

### This part of the repository focuses on the implementation of a Flask API and a WebSocket server, designed to facilitate communication between a Raspberry Pi-based client, controlling the LED-Strip, and an Ionic Vue-based GUI.

Before getting started, ensure that you have the following dependencies installed:
* Python 3.6 or higher
  
## Installation
Clone this repository to your local machine:

```bash 
git clone https://github.com/LetsGaming/LED-Controller-Websocket.git
cd LED-Controller-Websocket/Server
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
Review and update the configuration settings in the config.py file to match your specific setup.<br>
The API is, by default, running on all possible interfaces on port 5000 <br>
The Websocket Server also runs on all possible interfaces on port 8080

## Usage
Run the Flask API and WebSocket server:
```bash
python app.py
```
The server should now be running, ready to accept connections from both the Raspberry Pi client and the Ionic Vue-based GUI.

## API Endpoints
The Flask API provides the following endpoints:
TBD

## WebSocket Server
The WebSocket server is integrated into the Flask app and is used for real-time communication between the server and the Raspberry Pi client. WebSocket commands are defined in the commands.py file.
