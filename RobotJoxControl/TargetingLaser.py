"""
Wrapper for Targeting Laser component

Laser is controlled by single GPIO pin

Author: Aaron S. Crandall <crandall@gonzaga.edu>
Project: Robot Jox IoT NERF Robot
Copyright: 2023
"""


# Import necessary modules
import logging
import RPi.GPIO as GPIO


class TargetingLaser:
    """
    Class representing the targeting laser device of the Robot Jox IoT NERF Robot.

    Attributes:
    - gpio_pin (int): GPIO pin number for the laser device

    """

    def __init__(self, gpio_pin=5):
        """
        Initializes a TargetingLaser object with the given GPIO pin number.

        Args:
        - gpio_pin (int): GPIO pin number for the laser device
        """
        self.log = logging.getLogger(name=__class__.__name__)
        self.gpio_pin = gpio_pin
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self.log.info(f"Targeting laser online pin {self.gpio_pin}")

    def on(self):
        """
        Turns on the laser device.
        """
        GPIO.output(self.gpio_pin, GPIO.HIGH)
        self.log.debug("Targeting laser on")

    def off(self):
        """
        Turns off the laser device.
        """
        GPIO.output(self.gpio_pin, GPIO.LOW)
        self.log.debug("Targeting laser off")

    def command(self, type: str, options: list) -> None:
        """
        Executes a command on the laser device based on the command type and options provided.

        Args:
        - type (str): the type of command to execute ("on" or "off").
        - options (list): a list of command options (not used for this device).
        """
        if type == "on":
            self.on()
        elif type == "off":
            self.off()
