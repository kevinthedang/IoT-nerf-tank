
import logging
import threading
from time import sleep, time
import threading



class TreadMotor:
    def __init__(self, motorAPI, name):
        self.log = logging.getLogger(name=__class__.__name__ + "-" + name)

        self.motorAPI = motorAPI
        self.name = name
        self.log.info(f"Created TreadMotor: {name}")

        self.deadmanTimeout = 1.0
        self.lastControlEpoch = time()
        self.deadmanRunning = False
        self.deadmanThread = None

    def drive(self, speed=0):
        self.log.debug(f"{self.name} speed {speed}")
        self.motorAPI.throttle = speed
        self.lastControlEpoch = time()
        if not self.deadmanRunning:
            self.deadmanThread = threading.Thread(target=self.deadmanMethod)
            self.deadmanThread.start()

    def stop(self):
        self.motorAPI.throttle = 0

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

    def command(self, type: str, options: list) -> None:
        speed = float(options[0])
        if speed < -1 or speed > 1:
            self.log.warn(f"Speed sent out of range: {speed}")
        elif type == "drive":
            self.drive(speed=float(options[0]))



