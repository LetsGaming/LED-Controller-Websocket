import json
import logging
import os
from datetime import datetime, timedelta
from logging import Logger
import time

import pytz
import requests

class SunsetProvider():
    def __init__(self, sunset_config, call_at_sunset, logger: Logger):
        if not sunset_config['disable_provider']:
            self.logger = logger
            self.call_at_sunset = call_at_sunset
            self.time_zone = pytz.timezone(sunset_config['time_zone'])
            self.location = self._get_location(sunset_config)

            conf_turn_off_time = sunset_config['turn_off_time']
            if conf_turn_off_time:
                self.turn_off_time = self._format_turn_off_time(conf_turn_off_time)
            
            self.sunset_time = self._get_sunset_time()
            self._log_sunset_time()

    def _format_turn_off_time(self, time_str: str): 
        # Parse turn_off_time from config
        turn_off_time_format = "%H:%M"
        if ":" not in time_str:
            turn_off_time_format = "%H%M"
        elif time_str[-2:] == "AM" or time_str[-2:] == "PM":
            turn_off_time_format = "%I:%M %p"
        turn_off_time = datetime.strptime(time_str, turn_off_time_format).time()
        
        return datetime.combine(datetime.min, turn_off_time, self.time_zone)

    def _get_location(self, sunset_config):
        location = None
        if sunset_config['use_static']:
            static_location = sunset_config['static_location']
            location = Location(static_location[0], static_location[1])
            return location
        try:
            response = requests.get('http://ipinfo.io/json')
            data = response.json()
            # Extract latitude and longitude
            latitude, longitude = map(float, data['loc'].split(','))

            # Create Location object
            location = Location(latitude, longitude)
            return location
        except:
            return None

    def auto_activate_and_deactivate(self):
        while True:
            current_time = datetime.now(self.time_zone)

            # Check and activate at sunset
            if current_time >= self.sunset_time:
                self.call_at_sunset(True)
                # Update sunset time for the next day
                next_day = (current_time + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                self.sunset_time = self._get_sunset_time(next_day)
                self._log_sunset_time()

            # Check and deactivate at turn_off_time
            if self.turn_off_time:
                if current_time.hour == self.turn_off_time.hour and current_time.minute == self.turn_off_time.minute:
                    self.call_at_sunset(False)

            time.sleep(60)

    def _get_sunset_time(self, date=None):
        if self.location is not None:
            if date is None:
                date = datetime.now()

            latitude = self.location.latitude
            longitude = self.location.longitude
            
            formatted_date = date.strftime("%Y-%m-%d")
            
            url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={formatted_date}&formatted=0"
            response = requests.get(url)

            try:
                data = response.json()
                sunset_time_str = data['results']['sunset']
                
                # Parse sunset time string into naive datetime object
                sunset_time_data = datetime.fromisoformat(sunset_time_str[:-6]) # Remove timezone offset
                
                # Localize the naive datetime object with UTC timezone
                sunset_time = pytz.utc.localize(sunset_time_data)
                
                # Convert UTC time to the specified timezone
                sunset_time = sunset_time.astimezone(self.time_zone)
                
                return sunset_time
            except json.JSONDecodeError:
                self.logger.error("Unable to parse JSON response from OpenWeatherMap API")
                return None


    def _log_sunset_time(self):
        if self.sunset_time is not None:
            formatted_time = self.sunset_time.strftime("%d.%m.%Y %H:%M:%S")
            self.logger.info("Next sunset time: %s", formatted_time)
        else:
            self.logger.warning("Sunset time is not available.")

class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

def test_function(lean: bool):
    if lean:
        print("Sunset")
    else:
        print("Turn off")

def _init_logger():
    logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create a logger instance
    return logging.getLogger(__name__)

def load_config():
    """
    Load configuration from the 'config.json' file located in the same directory as this script.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")

    with open(config_path, 'r') as file:
        return json.load(file)

config = load_config()
LOGGER = _init_logger()

sunset_provider = SunsetProvider(config['sunset_provider'], test_function, LOGGER)
sunset_provider.auto_activate_and_deactivate()