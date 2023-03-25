
import logging
from gpiozero import AngularServo


class JoxServo:
    def __init__(self, name, gpio_pin):
        self.name = name
        self.gpio_pin = gpio_pin
        self.current_angle = 0
        self.minAngleRail = -90
        self.maxAngleRail = 90
        self.homeAngle = 0

        self.log = logging.getLogger(name=__class__.__name__ + "-" + self.name)

        self.servo = AngularServo(self.gpio_pin, min_pulse_width=0.0006, max_pulse_width=0.0023)
        self.log.info("Servo Enabled")

    def turnRight(self, degrees=10):
        self.current_angle -= degrees
        self.setAngle(self.current_angle)

    def turnLeft(self, degrees=10):
        self.current_angle += degrees
        self.setAngle(self.current_angle)

    def setAngle(self, newAngle):
        # Check for min/max?
        if newAngle < self.minAngleRail or newAngle > self.maxAngleRail:
            self.log.warn(f"Out of range angle sent: {newAngle}")
        else:
            self.log.debug(f"Servo angle is: {newAngle}")
            self.servo.angle = newAngle

    def setHome(self):
        self.log.debug("Returning Home Position")
        self.current_angle = self.homeAngle
        self.setAngle(self.current_angle)

    def command(self, type: str, options: list) -> None:
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
            self.setAngle(degrees=degrees)
        # ServoName:setHome
        elif type == "setHome":
            self.setHome()



