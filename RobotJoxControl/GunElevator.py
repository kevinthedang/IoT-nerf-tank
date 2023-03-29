"""
Gun Elevator class for controlling a servo motor to lift a gun up and down.

Project: IoT Driven NERF Robot: Robot Jox

Author: Aaron S. Crandall (crandall@gonzaga.edu)
Copyright: 2023

"""

from JoxServo import JoxServo


class GunElevator(JoxServo):
    def __init__(self, gpio_pin):
        """
        Constructor for GunElevator class. Inherits from JoxServo and initializes
        the default min and max angle ranges, as well as sets the initial angle
        to the home angle.

        :param gpio_pin: GPIO pin number for the servo motor
        """
        super().__init__(name="Gun Elevator", gpio_pin=gpio_pin)

        self.min_angle_rail = -0
        self.max_angle_rail = 20
        self.home_angle = 0
        self.current_angle = self.home_angle

    def up(self, degrees=10):
        """
        Method to lift the gun up by a specified number of degrees.

        :param degrees: The number of degrees to lift the gun
        """
        self.turnLeft(degrees)

    def down(self, degrees=10):
        """
        Method to lower the gun down by a specified number of degrees.

        :param degrees: The number of degrees to lower the gun
        """
        self.turnRight(degrees)

    def command(self, type: str, options: list) -> None:
        """
        Method to execute a command for the GunElevator. The commands include 'up',
        'down', 'setAngle', and 'setHome'.

        :param type: The type of command to execute
        :param options: A list of options for the command
        """
        if type == "up":
            degrees = float(options[0])
            self.up(degrees=degrees)
        if type == "down":
            degrees = float(options[0])
            self.down(degrees=degrees)
        # ServoName:setAngle:degrees
        elif type == "setAngle":
            degrees = float(options[0])
            self.setAngle(degrees=degrees)
        # ServoName:setHome
        elif type == "setHome":
            self.setHome()

