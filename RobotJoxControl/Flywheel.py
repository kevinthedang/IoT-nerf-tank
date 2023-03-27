
import logging
import threading
from time import sleep, time
import threading



class Flywheel:
    def __init__(self, motorAPIRightFlywheel, motorAPILeftFlywheel):
        name = "Flywheel"
        self.log = logging.getLogger(name=__class__.__name__ + "-" + name)

        self.motorAPIRightFlywheel = motorAPIRightFlywheel
        self.motorAPILeftFlywheel = motorAPILeftFlywheel
        self.name = name
        self.log.info(f"Created Flywheel: {name}")

        self.fireSpeed = 1.0
        self.offSpeed = 0.0
        self.readySpeed = 0.5

        self.deadmanTimeout = 5.0
        self.lastControlEpoch = time()
        self.deadmanRunning = False
        self.deadmanThread = None

    def drive(self, speed=0):
        self.log.debug(f"{self.name} speed {speed}")
        self.motorAPIRightFlywheel.throttle = speed
        self.motorAPILeftFlywheel.throttle = -1 * speed
        self.lastControlEpoch = time()
        if not self.deadmanRunning:
            self.deadmanThread = threading.Thread(target=self.deadmanMethod)
            self.deadmanThread.start()

    def stop(self):
        self.motorAPIRightFlywheel.throttle = self.offSpeed
        self.motorAPILeftFlywheel.throttle = self.offSpeed

    def deadmanMethod(self):
        self.deadmanRunning = True
        self.log.debug("Deadman started")
        while self.lastControlEpoch + self.deadmanTimeout >= time():
            sleep(self.deadmanTimeout)
        self.log.debug("Deadman done - stopping motor")
        self.stop()
        self.deadmanRunning = False

    def __del__(self):
        self.stop()

    def goToReady(self):
        self.log.debug("Going to ready speed")
        self.drive(speed=self.readySpeed)

    def goToFire(self):
        self.log.debug("Going to fire speed")
        self.drive(speed=self.fireSpeed)

    def command(self, type: str, options: list) -> None:
        if type == "stop":
            self.stop()
        elif type == "ready":
            self.goToReady()
        elif type == "fire":
            self.goToFire()



