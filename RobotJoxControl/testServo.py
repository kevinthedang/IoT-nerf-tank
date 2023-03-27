

from JoxServo import JoxServo
from time import sleep

from AmmoRammer import AmmoRammer
from GunElevator import GunElevator
from TurretRing import TurretRing


rammer = AmmoRammer(gpio_pin=16)
elevator = GunElevator(gpio_pin=13)
ring = TurretRing(gpio_pin=12)


#rammer.setHome()
#elevator.setHome()
#elevator.up(40)
ring.setHome()
sleep(0.5)
ring.setAngle(30)
#ring.turnLeft(10)
#ring.setHome()
sleep(1)
print("GoTime")
#rammer.fire()
#rammer.setAngle(-60)

sleep(2)


