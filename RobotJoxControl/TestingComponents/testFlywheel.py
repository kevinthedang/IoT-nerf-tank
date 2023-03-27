from time import sleep
import logging

from Flywheel import Flywheel

import board
from adafruit_motorkit import MotorKit

logging.basicConfig(level=logging.DEBUG)

motorKit = MotorKit(i2c=board.I2C())


flywheel = Flywheel(
    motorAPIRightFlywheel=motorKit.motor1, motorAPILeftFlywheel=motorKit.motor2
)

# flywheel.drive(speed=0.3)
flywheel.goToReady()

sleep(2)
flywheel.goToFire()
sleep(2)
flywheel.goToFire()
sleep(2)
flywheel.goToFire()
sleep(2)
flywheel.goToFire()
sleep(2)
flywheel.goToFire()
sleep(2)

flywheel.stop()

sleep(1)
