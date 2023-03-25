
from JoxServo import JoxServo


class GunElevator(JoxServo):
    def __init__(self, gpio_pin):
        super().__init__(name="Gun Elevator", gpio_pin=gpio_pin)

        # Initialize home angle to?
        # Min? Max?

        self.current_angle = 0
        self.minAngleRail = -90
        self.maxAngleRail = 90
        self.homeAngle = 0

        self.setHome()

    def up(self, degrees=10):
        self.turnRight(degrees)

    def down(self, degrees=10):
        self.turnLeft(degrees)

    def command(self, type: str, options: list) -> None:
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

