from datetime import datetime, timedelta
import json
import time
import pytz
import requests

from utils.logger import LOGGER

class SunsetProvider:
    def __init__(self, sunset_config, call_at_sunset):
        """
        Initializes the object with the given configuration and logger.
        
        Args:
            sunset_config (dict): A dictionary containing the sunset configuration.
            call_at_sunset (callable): A callback function to be called at sunset.
        """
        if not sunset_config.get('disable_provider', False):
            self.callback = call_at_sunset
            self.time_zone = pytz.timezone(sunset_config['time_zone'])
            self.location = self._get_location_with_retry(sunset_config)

            self.turn_on_time = self._parse_time(sunset_config.get('turn_on_time'), default_to_sunset=True)
            self.turn_off_time = self._parse_time(sunset_config.get('turn_off_time'))
            self.sunset_time = self._get_sunset_time_with_retry()

            self._log_times()

    def _parse_time(self, time_str: str, default_to_sunset=False):
        """
        Parses a time string into a datetime object in the configured time zone. 
        Supports formats "%H:%M", "%H%M", or "%I:%M %p". If the time_str is "sunset", returns sunset time.

        Args:
            time_str (str): Time string to parse.
            default_to_sunset (bool): Whether to default to sunset time if "sunset" is passed.

        Returns:
            datetime: Parsed datetime object or sunset if "sunset" is provided.
        """
        if not time_str:
            return None
        if time_str.lower() == "sunset" and default_to_sunset:
            return "sunset"
        
        time_formats = ["%H:%M", "%H%M", "%I:%M %p"]
        for fmt in time_formats:
            try:
                parsed_time = datetime.strptime(time_str, fmt).time()
                return datetime.combine(datetime.min, parsed_time, self.time_zone)
            except ValueError:
                continue
        LOGGER.error(f"Invalid time format: {time_str}")
        return None

    def _get_location(self, sunset_config):
        """
        Retrieves the location based on the sunset configuration.
        Uses static location if configured, otherwise attempts to fetch via IP.

        Returns:
            Location or None: Location object or None if it fails.
        """
        if sunset_config.get('use_static', False):
            static_location = sunset_config['static_location']
            return Location(static_location[0], static_location[1])

        try:
            response = requests.get('http://ipinfo.io/json')
            data = response.json()
            latitude, longitude = map(float, data['loc'].split(','))
            return Location(latitude, longitude)
        except Exception as e:
            LOGGER.error(f"Failed to retrieve location: {e}")
            return None

    def _get_location_with_retry(self, sunset_config):
        """ Continuously tries to get the location until it succeeds. """
        while True:
            location = self._get_location(sunset_config)
            if location:
                return location
            LOGGER.warning("Failed to get location, retrying in 30 seconds...")
            time.sleep(30)

    def _get_sunset_time(self, date=None):
        """
        Retrieves the sunset time for the specified date.

        Returns:
            datetime or None: Sunset time in the configured time zone.
        """
        if self.location:
            try:
                date = date or datetime.now()
                latitude, longitude = self.location.latitude, self.location.longitude
                formatted_date = date.strftime("%Y-%m-%d")
                
                url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={formatted_date}&formatted=0"
                response = requests.get(url)
                data = response.json()
                
                sunset_time_str = data['results']['sunset']
                sunset_time_utc = datetime.fromisoformat(sunset_time_str[:-6]).replace(tzinfo=pytz.utc)
                return sunset_time_utc.astimezone(self.time_zone)
            except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
                LOGGER.error(f"Error retrieving sunset time: {e}")
        return None

    def _get_sunset_time_with_retry(self, date=None):
        """ Continuously tries to get the sunset time until it succeeds. """
        while True:
            sunset_time = self._get_sunset_time(date)
            if sunset_time:
                return sunset_time
            LOGGER.warning("Failed to get sunset time, retrying in 30 seconds...")
            time.sleep(30)

    def auto_activate_and_deactivate(self):
        """ Continuously checks the current time and activates/deactivates accordingly. """
        while True:
            current_time = datetime.now(self.time_zone)

            # Turn on logic
            if self.turn_on_time == "sunset":
                if current_time >= self.sunset_time:
                    self.callback(True)
            elif self.turn_on_time and current_time.time() >= self.turn_on_time.time():
                self.callback(True)

            # Turn off logic
            if self.turn_off_time and current_time.time() >= self.turn_off_time.time():
                self.callback(False)

            # Update sunset time for next day
            if current_time >= self.sunset_time:
                next_day = current_time + timedelta(days=1)
                self.sunset_time = self._get_sunset_time_with_retry(next_day)
                self._log_times()

            time.sleep(60)

    def _log_times(self):
        """ Logs the sunset, turn-on, and turn-off times. """
        if self.sunset_time:
            LOGGER.info(f"Next sunset time: {self.sunset_time.strftime('%d.%m.%Y %H:%M:%S')}")
        if self.turn_on_time == "sunset":
            LOGGER.info("Turn on at sunset.")
        elif self.turn_on_time:
            LOGGER.info(f"Turn on time: {self.turn_on_time.strftime('%H:%M:%S')}")
        if self.turn_off_time:
            LOGGER.info(f"Turn off time: {self.turn_off_time.strftime('%H:%M:%S')}")

class Location:
    """ Represents a geographical location with latitude and longitude coordinates. """
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
