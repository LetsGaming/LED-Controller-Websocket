from datetime import datetime, timedelta
import json
import time

import pytz
import requests

from utils.logger import LOGGER

class SunsetProvider():
    def __init__(self, sunset_config, call_at_sunset):
        """
        Initializes the object with the given configuration and logger.

        Args:
            sunset_config (dict): A dictionary containing the sunset configuration.
            call_at_sunset (callable): A callback function to be called at sunset.
            logger (Logger): A logger object for logging purposes.

        Attributes:
            logger (Logger): The logger object.
            callback (callable): The callback function to be called at sunset.
            time_zone (pytz.timezone): The time zone of the location.
            location (str): The location for which the sunset time is calculated.
            turn_off_time (str): The time at which to turn off, if configured.
            sunset_time (str): The calculated sunset time.

        Notes:
            If `disable_provider` is set to `True` in the `sunset_config`, the object will not be initialized.
        """
        if not sunset_config['disable_provider']:
            self.callback = call_at_sunset
            self.time_zone = pytz.timezone(sunset_config['time_zone'])
            self.location = self._get_location(sunset_config)

            conf_turn_off_time = sunset_config['turn_off_time']
            if conf_turn_off_time:
                self.turn_off_time = self._format_turn_off_time(conf_turn_off_time)
                
            self.sunset_time = self._get_sunset_time_with_retry()
            self._log_sunset_time()
    
    def _format_turn_off_time(self, time_str: str):
        """
        Formats the turn off time string into a datetime object.

        Args:
        time_str (str): The turn off time string in one of the following formats: "%H:%M", "%H%M", or "%I:%M %p".

        Returns:
        datetime: A datetime object representing the turn off time in the configured time zone.

        Notes:
        The method automatically detects the format of the input string and parses it accordingly.
        """
        turn_off_time_format = "%H:%M"
        if ":" not in time_str:
            turn_off_time_format = "%H%M"
        elif time_str[-2:] == "AM" or time_str[-2:] == "PM":
            turn_off_time_format = "%I:%M %p"
        turn_off_time = datetime.strptime(time_str, turn_off_time_format).time()
        
        return datetime.combine(datetime.min, turn_off_time, self.time_zone)

    def _get_location(self, sunset_config):
        """
        Retrieves the location based on the sunset configuration.

        Args:
        sunset_config (dict): A dictionary containing the sunset configuration.

        Returns:
        Location or None: A Location object if the location can be determined, otherwise None.

        Notes:
        If 'use_static' is True in the sunset configuration, the method returns a Location object based on the 'static_location' coordinates.
        Otherwise, it attempts to retrieve the location from the 'http://ipinfo.io/json' API.
        """
        if sunset_config['use_static']:
            static_location = sunset_config['static_location']
            return Location(static_location[0], static_location[1])
        try:
            response = requests.get('http://ipinfo.io/json')
            data = response.json()
            latitude, longitude = map(float, data['loc'].split(','))
            return Location(latitude, longitude)
        except:
            return None

    def _get_sunset_time(self, date: datetime=None):
        """
        Retrieves the sunset time for the specified date and location.

        Args:
        date (datetime, optional): The date for which to retrieve the sunset time. Defaults to the current date.

        Returns:
        datetime or None: A datetime object representing the sunset time in the configured time zone, or None if the JSON response cannot be parsed.

        Notes:
        The method uses the sunrise-sunset API to retrieve the sunset time and converts it to the configured time zone.
        If the date is not specified, it defaults to the current date.
        """
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
                
                sunset_time_data = datetime.fromisoformat(sunset_time_str[:-6])
                sunset_time = pytz.utc.localize(sunset_time_data)
                sunset_time = sunset_time.astimezone(self.time_zone)
                
                return sunset_time
            except (json.JSONDecodeError, KeyError) as e:
                LOGGER.error("Unable to parse JSON response from sunrise-sunset API: %s", e)
                return None

    def _get_sunset_time_with_retry(self, date: datetime=None):
        """
        Continuously tries to get the sunset time until it succeeds.

        Args:
        date (datetime, optional): The date for which to retrieve the sunset time. Defaults to the current date.

        Returns:
        datetime: A datetime object representing the sunset time in the configured time zone.
        """
        while True:
            sunset_time = self._get_sunset_time(date)
            if sunset_time:
                return sunset_time
            LOGGER.warning("Failed to get sunset time, retrying in 30 seconds...")
            time.sleep(30)
    
    def auto_activate_and_deactivate(self):
        """
        Continuously checks the current time and activates/deactivates the callback accordingly.

        This method runs an infinite loop, checking the current time every 60 seconds.
        When the current time reaches the sunset time, it calls the callback with True as an argument.
        It then updates the sunset time for the next day.
        If a turn-off time is configured, it calls the callback with False as an argument when the current time matches the turn-off time.

        Notes:
        This method should be run in a separate thread or process to avoid blocking the main program.
        """
        while True:
            current_time = datetime.now(self.time_zone)

            if current_time >= self.sunset_time:
                self.callback(True)
                next_day = (current_time + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                self.sunset_time = self._get_sunset_time_with_retry(next_day)
                self._log_sunset_time()

            if self.turn_off_time:
                if current_time.hour == self.turn_off_time.hour and current_time.minute == self.turn_off_time.minute:
                    self.callback(False)

            time.sleep(60)

    def _log_sunset_time(self):
        """
        Logs the next sunset time.

        If the sunset time is available, it logs the time in the format "dd.mm.yyyy HH:MM:SS" using the logger's info level.
        If the sunset time is not available, it logs a warning message using the logger's warning level.
        """
        if self.sunset_time is not None:
            formatted_time = self.sunset_time.strftime("%d.%m.%Y %H:%M:%S")
            LOGGER.info("Next sunset time: %s", formatted_time)
        else:
            LOGGER.warning("Sunset time is not available.")

class Location:
    """
    Represents a geographical location with latitude and longitude coordinates.

    Attributes:
    latitude (float): The latitude of the location.
    longitude (float): The longitude of the location.
    """
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude