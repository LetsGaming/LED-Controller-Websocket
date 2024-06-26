import random
import time
from utils.utils import *

class Rainbow_Cycle(Animation):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    def __init__(self, strip):
        super().__init__(self._rainbow_cycle)
        self.strip = strip

    def _rainbow_cycle(self):
        try:
            self.animationStarted = True
            while not self.stopAnimation:
                for j in range(256 * 5):
                    if self.stopAnimation:
                        break
                    for i in range(self.strip.numPixels()):
                        if self.stopAnimation:
                            break
                        self.strip.setPixelColor(i, wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
                    self.strip.show()
                    time.sleep(0.02)
        except Exception as e:
            print(f"Something went wrong: {e}")
            return False

class Rainbow_Comet(Animation):
    """Create a comet effect with a rainbow tail that moves along the LED strip."""
    def __init__(self, strip):
        super().__init__(self._rainbow_comet)
        self.strip = strip

    def _rainbow_comet(self):
        try:
            num_pixels = self.strip.numPixels()
            tail_length = int((num_pixels * 5) / 100) 
            comet_speed = 0.1
            self.animationStarted = True
            while not self.stopAnimation:
                for i in range(num_pixels):
                    if self.stopAnimation:
                        break
                    for j in range(tail_length + 1):
                        if self.stopAnimation:
                            break
                        color = wheel((i + j) & 255)  # Get rainbow color based on pixel position
                        self.strip.setPixelColor(i - j, color)  # Set pixel color for the tail
                    self.strip.show()
                    time.sleep(comet_speed)
                    for j in range(tail_length + 1):
                        if self.stopAnimation:
                            break
                        self.strip.setPixelColor(i - j, 0)  # Clear tail pixels
        except Exception as e:
            print(f"Something went wrong: {e}")
            return False

class Theater_Chase_Rainbow(Animation):
    """Rainbow movie theater light style chaser animation."""
    def __init__(self, strip):
        super().__init__(self._theater_chase_rainbow)
        self.strip = strip

    def _theater_chase_rainbow(self):
        try:
            self.animationStarted = True
            while not self.stopAnimation:
                for j in range(256):
                    if self.stopAnimation:
                        break
                    for q in range(3):
                        if self.stopAnimation:
                            break
                        for i in range(0, self.strip.numPixels(), 3):
                            if self.stopAnimation:
                                break
                            self.strip.setPixelColor(i + q, wheel((i + j) % 255))
                        self.strip.show()
                        time.sleep(0.05)
                        for i in range(0, self.strip.numPixels(), 3):
                            if self.stopAnimation:
                                break
                            self.strip.setPixelColor(i + q, 0)
        except Exception as e:
            print(f"Something went wrong: {e}")
            return False
        
class Rainbow_Bounce(Animation):
    """Bounce a rainbow color back and forth across the LED strip."""
    def __init__(self, strip):
        super().__init__(self._rainbow_bounce)
        self.strip = strip
        self.position = 0
        self.direction = 1

    def _rainbow_bounce(self):
        try:
            num_pixels = self.strip.numPixels()
            self.animationStarted = True

            while not self.stopAnimation:
                for i in range(num_pixels):
                    if self.stopAnimation:
                        break
                    self.strip.setPixelColor(i, fade_wheel((i + self.position) & 255))

                self.strip.show()
                time.sleep(0.05)

                self.position += self.direction

                if self.position == num_pixels - 1 or self.position == 0:
                    self.direction *= -1  # Reverse direction when reaching the end

            for i in range(num_pixels):
                if self.stopAnimation:
                    break
                self.strip.setPixelColor(i, 0)

            self.strip.show()

        except Exception as e:
            print(f"Something went wrong: {e}")
            return False

class Random_Bounce(Animation):
    """Bounce a random color back and forth across the LED strip."""
    def __init__(self, strip):
        super().__init__(self._color_bounce)
        self.strip = strip
        self.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.position = 0
        self.direction = 1

    def _color_bounce(self):
        try:
            num_pixels = self.strip.numPixels()
            self.animationStarted = True

            while not self.stopAnimation:
                for i in range(num_pixels):
                    if self.stopAnimation:
                        break
                    self.strip.setPixelColor(i, 0)

                # Fade out the previous position
                prev_position = (self.position - self.direction) % num_pixels
                self.strip.setPixelColor(prev_position, Color(
                    int(self.color.r * 0.8),
                    int(self.color.g * 0.8),
                    int(self.color.b * 0.8)
                ))

                # Set the current position with the full color
                self.strip.setPixelColor(self.position, self.color)
                self.strip.show()
                time.sleep(0.05)

                # Fade in the next position
                next_position = (self.position + self.direction) % num_pixels
                self.strip.setPixelColor(next_position, Color(
                    int(self.color.r * 0.8),
                    int(self.color.g * 0.8),
                    int(self.color.b * 0.8)
                ))

                self.position += self.direction

                if self.position == num_pixels - 1 or self.position == 0:
                    self.direction *= -1  # Reverse direction when reaching the end

            for i in range(num_pixels):
                if self.stopAnimation:
                    break
                self.strip.setPixelColor(i, 0)

            self.strip.show()

        except Exception as e:
            print(f"Something went wrong: {e}")
            return False