
from JoxServo import JoxServo


class TurretRing(JoxServo):
    def __init__(self, gpio_pin):
        super().__init__(name="Turret Ring", gpio_pin=gpio_pin)

        self.minAngleRail = -90
        self.maxAngleRail = 90
        self.homeAngle = 0
        self.current_angle = self.homeAngle

