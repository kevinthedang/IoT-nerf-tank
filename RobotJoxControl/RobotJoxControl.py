#!/usr/bin/python3
"""
Main program for the Robot Jox hardware control service

Author: Aaron S. Crandall <crandall@gonzaga.edu>
Project: Robot Jox IoT NERF Robot
Copyright: 2023
"""

# Built-in Python libs
import logging
from time import sleep

# Special Project depencies
import board
from adafruit_motorkit import MotorKit
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Project Classes
from TargetingLaser import TargetingLaser
from TreadMotor import TreadMotor
from GunElevator import GunElevator
from AmmoRammer import AmmoRammer
from TurretRing import TurretRing
from Flywheel import Flywheel


# ***************************************************************** #
def on_mqtt_message(client, userdata, message):
    """
    Callback function that is executed when a message is received from the MQTT broker.

    :param client: The MQTT client instance.
    :type client: paho.mqtt.client.Client
    :param userdata: The user data passed to the callback.
    :param message: An object containing the message payload, topic, QoS, and retain flag.
    :type message: paho.mqtt.client.MQTTMessage
    """
    message = message.payload.decode()
    message = message.strip()
    logging.debug(f"Control: {message}")

    commandFields = message.split(":")
    deviceName = commandFields[0]
    commandType = commandFields[1]
    commandOptions = commandFields[2:]

    if deviceName in robotDevices:
        robotDevices[deviceName].command(commandType, commandOptions)
    else:
        logging.warn(f"Control of unknown device: {deviceName} - {message}")


def setupMQTTClient() -> mqtt.Client:
    """
    Sets up and returns an instance of the MQTT client.

    :return: An instance of the MQTT client.
    :rtype: paho.mqtt.client.Client
    """
    mqttClient = mqtt.Client()
    mqttClient.connect("localhost", 1883)
    mqttClient.subscribe("control")
    mqttClient.on_message = on_mqtt_message
    return mqttClient


def setupRobotDevices() -> dict:
    """
    Sets up and returns a dictionary of the robot's devices.

    :return: A dictionary containing the robot's devices.
    :rtype: dict
    """
    global robotDevices
    motorKit = MotorKit(i2c=board.I2C())

    leftTread = TreadMotor(motorAPI=motorKit.motor3, name="left")
    rightTread = TreadMotor(motorAPI=motorKit.motor4, name="right")
    flywheel = Flywheel(
       motorAPIRightFlywheel=motorKit.motor1, motorAPILeftFlywheel=motorKit.motor2
    )
    targetingLaser = TargetingLaser(gpio_pin=5)
    turretRing = TurretRing(gpio_pin=12)
    gunElevator = GunElevator(gpio_pin=13)
    ammoRammer = AmmoRammer(gpio_pin=16)

    robotDevices["leftTread"] = leftTread
    robotDevices["rightTread"] = rightTread
    robotDevices["flywheel"] = flywheel
    robotDevices["targetingLaser"] = targetingLaser
    robotDevices["turretRing"] = turretRing
    robotDevices["gunElevator"] = gunElevator
    robotDevices["ammoRammer"] = ammoRammer

    return robotDevices


# ************************************************************************** #
if __name__ == "__main__":
    global robotDevices
    robotDevices = {}

    FORMAT = "%(asctime)s.%(msecs)03d;%(levelname)s;%(name)s:%(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt="%H:%M:%S")

    logging.info("Log started")

    mqttClient = setupMQTTClient()
    robotDevices = setupRobotDevices()

    try:
        mqttClient.loop_forever()
    except KeyboardInterrupt:
        logging.info("Received keyboard interrupt - quitting.")
    finally:
        mqttClient.disconnect()

        robotDevices["leftTread"].stop()
        robotDevices["rightTread"].stop()

    logging.info("Done.")
