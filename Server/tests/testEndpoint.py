import requests
import json

# Define the API endpoint URL for getting connected controllers
base_domain = "http://192.168.2.128:5000"
connected_controller_url = f"{base_domain}/led/connected_controller"

# Make a GET request to get the connected controllers
connected_controller_response = requests.get(connected_controller_url)

# Check the response
if connected_controller_response.status_code == 200:
    connected_controllers = connected_controller_response.json()

    # Check if there are connected controllers
    if connected_controllers:
        
        # Use the first connected controller ID
        # Extracting the first key under 'data'
        first_key = next(iter(connected_controllers['data']))

        # Accessing the ID using the first key
        controller_id = connected_controllers['data'][first_key]['id']
        
        turn_on_url = f"{base_domain}/led/set_online_state/{controller_id}"
        
        online_data = {
            'online': True
        }
        
        # Define the API endpoint URL for setting custom color
        custom_color_url = f"{base_domain}/led/animations/special/scanner_effect/{controller_id}"

        # Set the color values
        color_data = {
            'red': 255, 'green': 0, 'blue': 0, 'scan_speed': 5, 'tail_length': 10
        }

        requests.post(turn_on_url, json=online_data)
        # Make the POST request
        response = requests.post(custom_color_url, json=color_data)

        # Check the response
        if response.status_code == 200:
            print("Command sent successfully")
        else:
            print(f"Failed to send command. Status code: {response.status_code}")
            print(response.text)
    else:
        print("No connected controllers found")
else:
    print(f"Failed to get connected controllers. Status code: {connected_controller_response.status_code}")
    print(connected_controller_response.text)
