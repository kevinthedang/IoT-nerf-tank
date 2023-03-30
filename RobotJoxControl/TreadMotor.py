"""
Class for a motor controlling a tank tread - DC Motor Driven

This class wraps behaviors of the Adafruit RPi Motor Hat.
Allows for driving the motor at a specified speed, as well
as stopping the motor. It also implements a deadman switch
to stop the motor if it hasn't received a control signal
within a certain time frame.

Author: Aaron S. Crandall <crandall@gonzaga.edu>
Project: Robot Jox IoT NERF Robot
Copyright: 2023
"""

import logging
import threading
from time import sleep, time
import threading


class TreadMotor:
    def __init__(self, motorAPI, name: str):
        """
        Constructor for the TreadMotor class.
        :param motorAPI: The Adafruit RPi Motor Hat motor API
        :type motorAPI: object
        :param name: A name to associate with the motor
        :type name: str
        """

        self.log = logging.getLogger(name=__class__.__name__ + "-" + name)

        self.motorAPI = motorAPI
        self.name = name
        self.log.info(f"Created TreadMotor: {name}")

        self.deadmanTimeout = 1.0
        self.lastControlEpoch = time()
        self.deadmanRunning = False
        self.deadmanThread = None

    def drive(self, speed: int = 0) -> None:
        """
        Drives the motor at the specified speed.

        :param speed: The speed at which to drive the motor. Default 0.
        :type speed: float
        """

        self.log.debug(f"{self.name} speed {speed}")
        self.motorAPI.throttle = speed
        self.lastControlEpoch = time()
        if not self.deadmanRunning:
            self.deadmanThread = threading.Thread(target=self.deadmanMethod)
            self.deadmanThread.start()

    def stop(self) -> None:
        """ Stops the motor. """
        self.motorAPI.throttle = 0

    def deadmanMethod(self) -> None:
        """
        Method that monitors the motor for control signals. If no control
        signals are received for a certain amount of time, the motor is stopped.
        """
        self.deadmanRunning = True
        self.log.debug("Deadman started")
        while self.lastControlEpoch + self.deadmanTimeout >= time():
            sleep(self.deadmanTimeout)
        self.log.debug("Deadman done - stopping motor")
        self.stop()
        self.deadmanRunning = False

    def __del__(self) -> None:
        """ Destructor for the TreadMotor class. Stops the motor.  """
        self.stop()

    def command(self, type: str, options: list) -> None:
        """
        Executes a command on the motor.

        :param type: The type of command to execute.
        :type type: str
        :param options: The options to use when executing the command.
        :type options: list
        """
        speed = float(options[0])
        if speed < -1 or speed > 1:
            self.log.warn(f"Speed sent out of range: {speed}")
        elif type == "drive":
            self.drive(speed=float(options[0]))
