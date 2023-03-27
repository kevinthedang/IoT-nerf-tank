"""
Turret Ring object class for the Robot Jox NERF robot

Wraps the JoxServer class to put the proper limits on the turret ring servo.

Author: Aaron S. Crandall <crandall@gonzaga.edu>
Project: Robot Jox IoT NERF Robot
Copyright: 2023
"""

from JoxServo import JoxServo


class TurretRing(JoxServo):
    """Represents a Turret Ring that inherits from JoxServo class."""

    def __init__(self, gpio_pin: int):
        """Initializes a new instance of the TurretRing class.

        Args:
            gpio_pin (int): GPIO pin number used for the servo motor.
        """

        # Call the base class constructor to initialize the servo
        super().__init__(name="Turret Ring", gpio_pin=gpio_pin)

        self.minAngleRail = -90
        self.maxAngleRail = 90
        self.homeAngle = 0
        self.current_angle = self.homeAngle
