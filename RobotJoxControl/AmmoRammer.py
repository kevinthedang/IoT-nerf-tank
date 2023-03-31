"""
Ammo Rammer class for controlling a servo motor to push ammunition into a NERF gun.

Author: Aaron S. Crandall <crandall@gonzaga.edu>
Project: Robot Jox IoT NERF Robot
Copyright: 2023
"""

from time import sleep
from JoxServo import JoxServo


class AmmoRammer(JoxServo):
    def __init__(self, gpio_pin):
        """
        Constructor for AmmoRammer class. Inherits from JoxServo and overrides
        the default min and max angle ranges to match the physical specifications
        of the ammo rammer.

        :param gpio_pin: GPIO pin number for the servo motor
        """
        super().__init__(name="Ammo Rammer", gpio_pin=gpio_pin)

        self.min_angle_rail = -65
        self.max_angle_rail = 10
        self.home_angle = 10
        self.current_angle = self.home_angle

        self.fire_ram_angle_in = -65
        self.fire_ram_angle_back = self.home_angle
        self.fire_wait_time = 0.5

    def fire(self) -> None:
        """
        Method to fire the ammo rammer by pushing the ammunition forward and then back.

        :return: None
        """
        self.setAngle(self.fire_ram_angle_in)
        sleep(self.fire_wait_time)  # Blocking issue, stalls MQTT processing
        self.setAngle(self.fire_ram_angle_back)

    def command(self, type: str, options: list) -> None:
        """
        Method to execute a command for the AmmoRammer. The commands include 'fire'
        and 'setHome'.

        :param type: The type of command to execute
        :param options: A list of options for the command
        """
        # ammoRammer:fire
        if type == "fire":
            self.fire()
        # ammoRammer:setHome
        elif type == "setHome":
            self.set_home()
