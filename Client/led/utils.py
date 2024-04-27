import json
import time
from datetime import datetime, timedelta
import pytz
from logging import Logger
import requests

def validate_rgb_values(red, green, blue):
    try:
        red = int(red)
        green = int(green)
        blue = int(blue)
        if is_within_range(red, 0, 255) and is_within_range(green, 0, 255) and is_within_range(blue, 0, 255):
            return True
        else: return False
    except ValueError:
        return False   
     
def is_within_range(value, range_start, range_end):
    """Checks if a given value is within a specified range."""
    return range_start <= value <= range_end

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def custom_wheel(pos, colors):
    """Generate custom colors across 0-255 positions."""
    num_colors = len(colors)
    color_segment = 255 // (num_colors - 1)
    segment = min(pos // color_segment, num_colors - 2)
    remainder = pos % color_segment
    color_start = colors[segment]
    color_end = colors[segment + 1]
    r = color_start[0] + (color_end[0] - color_start[0]) * remainder // color_segment
    g = color_start[1] + (color_end[1] - color_start[1]) * remainder // color_segment
    b = color_start[2] + (color_end[2] - color_start[2]) * remainder // color_segment
    return Color(r, g, b)

def fade_wheel(wheel_value):
    """Apply fading effect to the rainbow color."""
    brightness = 0.8  # Adjust the fade factor as needed
    color = wheel(wheel_value)
    return Color(
        int(color.r * brightness),
        int(color.g * brightness),
        int(color.b * brightness)
    )

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
        
class Animation():
    def __init__(self, animation_func):
        self._animation_func = animation_func
        self.stopAnimation = True
        self.is_running = False
        self.animationStarted = False

    def start(self):
        self.stopAnimation = False
        self.is_running = True
        self._animation_func()
        self.is_running = False
        
    def stop(self):
        self.stopAnimation = True
        while self.is_running:
            time.sleep(0.1)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, 0)
        self.strip.show()

    def isStarted(self):
        return self.animationStarted

"""
    Same as in rpi_ws281x.Color and rpi_ws281x.RGBW
    This was copied and pasted to decrease needed imports
    I take no credit for these Functions!
"""
class RGBW(int):
    def __new__(self, r, g=None, b=None, w=None):
        if (g, b, w) == (None, None, None):
            return int.__new__(self, r)
        else:
            if w is None:
                w = 0
            return int.__new__(self, (w << 24) | (r << 16) | (g << 8) | b)

    @property
    def r(self):
        return (self >> 16) & 0xff

    @property
    def g(self):
        return (self >> 8) & 0xff

    @property
    def b(self):
        return (self) & 0xff

    @property
    def w(self):
        return (self >> 24) & 0xff


def Color(red, green, blue, white=0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return RGBW(red, green, blue, white)