"""
Server Wrapper/control class for controlling a servo motor.

Author: Aaron S. Crandall <crandall@gonzaga.edu>
Project: Robot Jox IoT NERF Robot
Copyright: 2023
"""


import logging
from gpiozero import AngularServo


class JoxServo:
    def __init__(self, name, gpio_pin):
        # Constructor for JoxServo class
        # name: name of the servo
        # gpio_pin: GPIO pin to which the servo is connected
        self.name = name
        self.gpio_pin = gpio_pin
        self.current_angle = 0
        self.minAngleRail = -90
        self.maxAngleRail = 90
        self.homeAngle = 0

        self.log = logging.getLogger(name=__class__.__name__ + "-" + self.name)

        self.servo = AngularServo(
            self.gpio_pin, min_pulse_width=0.0006, max_pulse_width=0.0023
        )
        self.log.info("Servo Enabled")

    def turnRight(self, degrees=10):
        # Turns the servo to the right by the given degrees
        # degrees: number of degrees to turn the servo to the right (default 10)
        self.current_angle -= degrees
        self.setAngle(self.current_angle)

    def turnLeft(self, degrees=10):
        # Turns the servo to the left by the given degrees
        # degrees: number of degrees to turn the servo to the left (default 10)
        self.current_angle += degrees
        self.setAngle(self.current_angle)

    def setAngle(self, newAngle):
        # Sets the servo angle to the given angle, if it is within the range
        # newAngle: the angle to set the servo to
        if newAngle < self.minAngleRail or newAngle > self.maxAngleRail:
            self.log.warn(f"Out of range angle sent: {newAngle}")
        else:
            self.log.debug(f"Servo angle is: {newAngle}")
            self.servo.angle = newAngle

    def setHome(self):
        # Sets the servo angle to the home angle
        self.log.debug("Returning Home Position")
        self.current_angle = self.homeAngle
        self.setAngle(self.current_angle)

    def command(self, type: str, options: list) -> None:
        # Executes the given command on the servo
        # type: the type of command to execute
        # options: the list of options for the command
        # ServoName:turnRight:degrees
        if type == "turnRight":
            degrees = float(options[0])
            self.turnRight(degrees=degrees)
        # ServoName:turnLeft:degrees
        elif type == "turnLeft":
            degrees = float(options[0])
            self.turnLeft(degrees=degrees)
        # ServoName:setAngle:degrees
        elif type == "setAngle":
            degrees = float(options[0])
            self.setAngle(newAngle=degrees)
        # ServoName:setHome
        elif type == "setHome":
            self.setHome()
