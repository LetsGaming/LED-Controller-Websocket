import threading
import time
from logging import Logger
from rpi_ws281x import *
from led.animations.startAnimations import *
from led.animations.standardAnimations import *
from led.animations.customAnimations import *
from led.animations.specialAnimations import *

OFFLINE_ERROR = "The LED-Strip is turned OFF!"

class LEDController():
    def __init__(self, logger: Logger, strip_config, sunset_config):
        self.logger = logger
        self.strip_config = strip_config

        self.strip = Adafruit_NeoPixel(strip_config["LED_COUNT"], strip_config["LED_PIN"], strip_config["LED_FREQ_HZ"], strip_config["LED_DMA"], strip_config["LED_INVERT"], strip_config["LED_BRIGHTNESS"], strip_config["LED_CHANNEL"])
        self.strip.begin()
        self.isOnline = False

        self.current_animation = None
        self.paused_animation = None
        self.animation_event = threading.Event()

        # Start with a startup animation and then clearing the strip
        self.run_startup_animation(self.strip_config["LED_BRIGHTNESS"])
        
        # Start the sunset activation loop in a separate thread
        sunset_provider = SunsetProvider(sunset_config, self.set_online_state, self.logger)
        self.sunset_activation_thread = threading.Thread(target=sunset_provider.auto_activate_and_deactivate)
        self.sunset_activation_thread.start()
        self.logger.info("Started LED-Controller")
        
    def run_startup_animation(self, brightness):
        self.clear_strip()
        color = (0, 255, 0)
        start_time = time.time()
        duration_ms = 2250
        end_time = start_time + (duration_ms / 1000.0)
        fade_interval = 1.0 / brightness

        while time.time() < end_time:
            elapsed = time.time() - start_time
            brightness = min(1.0, elapsed / (duration_ms / 1000.0))

            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(int(color[0] * brightness), int(color[1] * brightness), int(color[2] * brightness)))
            self.strip.show()
            time.sleep(fade_interval)

        self.clear_strip()

    def clear_strip(self):
        dark = Color(0, 0, 0)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, dark)
        self.strip.show()

    def get_online_state(self):
        return self.isOnline

    def set_online_state(self, value: bool):
        """Sets whether or not this device should be considered online by other devices."""
        try:
            if self.isOnline != value:
                self.isOnline = value
                if value and self.paused_animation is not None:
                    self._resume_animation()
                elif not value and self.paused_animation is None:
                    self._pause_animation()
                return True
        except Exception as e:
            self.logger.error("Error setting Online State:", str(e))
        return False

    def _pause_animation(self):
        self.paused_animation = self.current_animation
        self._stop_current_animation()

    def _resume_animation(self):
        if self.paused_animation is not None:
            self._start_animation(self.paused_animation)
        self.paused_animation = None

    def _stop_current_animation(self):
        """Stops the currently running animation if any."""
        if self.current_animation is not None:
            self.current_animation.stop()
            self.current_animation = None
        self.animation_event.set()  # Signal that animation has stopped

    def _start_animation(self, animation: Animation):
        """Starts a new animation after stopping the current animation."""
        self._stop_current_animation()
        self.animation_event.wait()  # Wait for animation to stop
        self.animation_event.clear()  # Reset the event for the next animation
        self.current_animation = animation
        animation_thread = threading.Thread(target=self.current_animation.start)
        animation_thread.start()

    def _is_animation_started(self):
        """Returns True if an animation is currently running."""
        return self.current_animation.isStarted()

    def get_brightness(self):
        """Returns the current strip's brightness level (between 0-255)."""
        if self.isOnline:
            return self.strip.getBrightness()
        else:
            return OFFLINE_ERROR

    def set_brightness(self, brightness):
        try:
            if self.isOnline:
                new_brightness = int(brightness)
                if 0 <= new_brightness <= 255:
                    self.strip.setBrightness(new_brightness)
                    self.strip.show()
                    return True
                else:
                    self.logger.warn("Value not between allowed range")
                    return False
            else:
                return OFFLINE_ERROR
        except Exception as e:
            self.logger.error("Error setting brightness: ", str(e))
            return False

    def _handle_animation(self, animation: Animation):
        if self.isOnline:
            self._start_animation(animation)
            return self._is_animation_started()
        else:
            return OFFLINE_ERROR

    # Start Animations
    def set_white(self):
        return self._handle_animation(SetWhite(self.strip))

    def fill_color(self, red, green, blue):
        return self._handle_animation(FillColor(self.strip, red, green, blue))

    def custom_fill(self, red, green, blue, percentage):
        return self._handle_animation(CustomFill(self.strip, red, green, blue, percentage))

    # Special Animations
    def blink(self, red, green, blue, blinking_speed):
        return self._handle_animation(Blink(self.strip, red, green, blue, blinking_speed))

    def fade(self, from_red, from_green, from_blue, to_red, to_green, to_blue, steps, fading_speed):
        return self._handle_animation(
            Fade(self.strip, from_red, from_green, from_blue, to_red, to_green, to_blue, steps, fading_speed))

    def sparkle(self, red, green, blue, sparkle_count):
        return self._handle_animation(Sparkle(self.strip, red, green, blue, sparkle_count))

    def scanner_effect(self, red, green, blue, scan_speed, tail_length):
        return self._handle_animation(ScannerEffect(self.strip, red, green, blue, scan_speed, tail_length))

    def yoyo_theater(self, red, green, blue, yoyo_speed):
        return self._handle_animation(YoyoTheater(self.strip, red, green, blue, yoyo_speed))

    def breathing_effect(self, red, green, blue, breathing_duration):
        return self._handle_animation(Breathing_Effect(self.strip, red, green, blue, breathing_duration))

    def color_ripple(self, red, green, blue, ripple_speed):
        return self._handle_animation(Color_Ripple(self.strip, red, green, blue, ripple_speed))
    
    # Custom Animations
    def color_wipe(self, red, green, blue):
        return self._handle_animation(Color_Wipe(self.strip, red, green, blue))

    def theater_chase(self, red, green, blue):
        return self._handle_animation(Theater_Chase(self.strip, red, green, blue))

    def strobe(self, red, green, blue):
        return self._handle_animation(Strobe(self.strip, red, green, blue))

    def color_chase(self, red, green, blue):
        return self._handle_animation(Color_Chase(self.strip, red, green, blue))

    def custom_rainbow_cycle(self, colors):
        return self._handle_animation(Custom_Rainbow_Cycle(self.strip, colors))
    
    #Standard Animations
    def rainbow_cycle(self):
        return self._handle_animation(Rainbow_Cycle(self.strip))

    def rainbow_comet(self):
        return self._handle_animation(Rainbow_Comet(self.strip))

    def theater_chase_rainbow(self):
        return self._handle_animation(Theater_Chase_Rainbow(self.strip))

    def rainbow_bounce(self):
        return self._handle_animation(Rainbow_Bounce(self.strip))

    def random_bounce(self):
        return self._handle_animation(Random_Bounce(self.strip))