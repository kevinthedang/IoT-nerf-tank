
from JoxServo import JoxServo


class GunElevator(JoxServo):
    def __init__(self, gpio_pin):
        super().__init__(name="Gun Elevator", gpio_pin=gpio_pin)

        self.minAngleRail = -0
        self.maxAngleRail = 40
        self.homeAngle = 0
        self.current_angle = self.homeAngle


    def up(self, degrees=10):
        self.turnLeft(degrees)

    def down(self, degrees=10):
        self.turnRight(degrees)

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

