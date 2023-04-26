"""
Module: Flywheel
Author: Aaron S. Crandall <crandall@gonzaga.edu>
Project: Robot Jox IoT NERF Robot
Copyright: 2023

This module defines the Flywheel class that controls the motors
of the flywheels on the NERF robot.
"""

import logging
import threading
from time import sleep, time


class Flywheel:
    def __init__(self, motorAPIRightFlywheel, motorAPILeftFlywheel):
        """
        Initializes the Flywheel object.

        Args:
            motorAPIRightFlywheel (MotorAPI): Right motor API for the flywheel.
            motorAPILeftFlywheel (MotorAPI): Left motor API for the flywheel.
        """
        name = "Flywheel"
        self.log = logging.getLogger(name=__class__.__name__ + "-" + name)

        self.motorAPIRightFlywheel = motorAPIRightFlywheel
        self.motorAPILeftFlywheel = motorAPILeftFlywheel
        self.name = name
        self.log.info(f"Created Flywheel: {name}")

        # Default motor speeds
        self.fireSpeed = 1.0
        self.offSpeed = 0.0
        self.readySpeed = 0.5

        # Deadman switch timeout
        self.deadmanTimeout = 5.0
        self.lastControlEpoch = time()
        self.deadmanRunning = False
        self.deadmanThread = None

    def drive(self, speed=0) -> None:
        """
        Sets the motor speeds for the flywheel.

        Args:
            speed (float): Speed to set for the motors (default 0).
        """
        self.log.debug(f"{self.name} speed {speed}")
        self.motorAPIRightFlywheel.throttle = speed
        self.motorAPILeftFlywheel.throttle = 1 * speed
        self.lastControlEpoch = time()
        if not self.deadmanRunning:
            self.deadmanThread = threading.Thread(target=self.deadmanMethod)
            self.deadmanThread.start()

    def stop(self) -> None:
        """Stops the flywheel motors."""
        self.motorAPIRightFlywheel.throttle = self.offSpeed
        self.motorAPILeftFlywheel.throttle = self.offSpeed

    def deadmanMethod(self) -> None:
        """Method for deadman switch to stop motor if no more drive commands arrive."""
        self.deadmanRunning = True
        self.log.debug("Deadman started")
        while self.lastControlEpoch + self.deadmanTimeout >= time():
            sleep(self.deadmanTimeout)
        self.log.debug("Deadman done - stopping motor")
        self.stop()
        self.deadmanRunning = False

    def __del__(self) -> None:
        """Destructor to stop the flywheel motor. Should always stop on destruction."""
        self.stop()

    def goToReady(self) -> None:
        """Sets the flywheel motors to the ready speed."""
        self.log.debug("Going to ready speed")
        self.drive(speed=self.readySpeed)

    def goToFire(self) -> None:
        """Sets the flywheel motors to the firing speed."""
        self.log.debug("Going to fire speed")
        self.drive(speed=self.fireSpeed)

    def command(self, type: str, options: list) -> None:
        """
        Executes the specified command for the flywheel.

        Args:
            type (str): Type of command to execute.
            options (list): List of options for the command.
        """
        if type == "stop":
            self.stop()
        elif type == "ready":
            self.goToReady()
        elif type == "fire":
            self.goToFire()
