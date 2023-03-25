
import logging
import RPi.GPIO as GPIO

class TargetingLaser:
    def __init__(self, gpio_pin=5):
        self.log = logging.getLogger(name=__class__.__name__)
        self.gpio_pin = gpio_pin
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self.log.info(f"Targeting laser online pin {self.gpio_pin}")

    def on(self):
        GPIO.output(self.gpio_pin, GPIO.HIGH)
        self.log.debug("Targeting laser on")

    def off(self):
        GPIO.output(self.gpio_pin, GPIO.LOW)
        self.log.debug("Targeting laser off")

    def command(self, type: str, options: list) -> None:
        if type == "on":
            self.on()
        elif type == "off":
            self.off()