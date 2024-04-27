LED-Controller-Websocket Client
This project involves the control and management of an LED strip using a WebSocket server and a sunset provider. The project utilizes the provided configuration to set up the LED strip and connect to the WebSocket server.

# LED Strip Configuration
The LED strip is configured with the following parameters:

* LED_COUNT: The number of LEDs in the strip.
* LED_PIN: The GPIO pin used to control the LED strip.
* LED_FREQ_HZ: The frequency of the LED signal.
* LED_DMA: The DMA (Direct Memory Access) channel used for the LED signal.
* LED_BRIGHTNESS: The maximum brightness of the LEDs.
* LED_INVERT: A flag indicating whether the LED signal is inverted.
* LED_CHANNEL: The PWM (Pulse Width Modulation) channel used for the LED signal.

# WebSocket Server Configuration
The WebSocket server is configured with the following parameters:

* server_address: The IP address of the WebSocket server.
* server_port: The port number used by the WebSocket server.

# Sunset Provider Configuration
The sunset provider is configured with the following parameters:

* disable_provider: A flag indicating whether the sunset provider should be used at all.
* openweathermap_api_key: The API key used to access the OpenWeatherMap service. @see https://openweathermap.org/api
* time_zone: The time zone used for the sunset time calculation.
* use_static: A flag indicating whether to use a static location for the sunset time calculation.
* static_location: The static location used for the sunset time calculation (latitude and longitude).
* turn_off_time: The time at which the LED strip should be turned off. Either 24h or 12h format

# Usage
To use this project, follow these steps:

* Configure the LED strip, WebSocket server, and sunset provider using the provided parameters.
* Connect to the WebSocket server and send commands to control the LED strip.
* Use the sunset provider to calculate the sunset time and adjust the LED strip brightness accordingly.