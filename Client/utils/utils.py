import time

from utils.logger import LOGGER

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