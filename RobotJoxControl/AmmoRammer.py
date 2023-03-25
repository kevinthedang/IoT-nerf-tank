
from time import sleep

from JoxServo import JoxServo


class AmmoRammer(JoxServo):
    def __init__(self, gpio_pin):
        super().__init__(name="Ammo Rammer", gpio_pin=gpio_pin)

        # Override defaults for rammer physical specifications
        self.current_angle = -60
        self.minAngleRail = -90
        self.maxAngleRail = -60
        self.homeAngle = -60

        self.fireRamAngleIn = self.minAngleRail
        self.fireRamAngleBack = self.maxAngleRail
        self.fireWaitTime = 0.5

        self.setHome()

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

