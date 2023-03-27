
from time import sleep

from JoxServo import JoxServo


class AmmoRammer(JoxServo):
    def __init__(self, gpio_pin):
        super().__init__(name="Ammo Rammer", gpio_pin=gpio_pin)

        # Override defaults for rammer physical specifications
        # All experimentally determined
        self.minAngleRail = -65
        self.maxAngleRail = 20
        self.homeAngle = 20
        self.current_angle = self.homeAngle

        self.fireRamAngleIn = -65
        self.fireRamAngleBack = self.homeAngle
        self.fireWaitTime = 0.5


    def fire(self):
        self.setAngle(self.fireRamAngleIn)
        sleep(self.fireWaitTime)     # Blocking issue, stalls MQTT processing
        self.setAngle(self.fireRamAngleBack)


    def command(self, type: str, options: list) -> None:
        # ammoRammer:fire
        if type == "fire":
            self.fire()
        # ammoRammer:setHome
        elif type == "setHome":
            self.setHome()


