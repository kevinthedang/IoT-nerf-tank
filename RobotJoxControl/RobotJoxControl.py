#!/usr/bin/python3

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
from JoxServo import JoxServo
from GunElevator import GunElevator
from AmmoRammer import AmmoRammer


# ***************************************************************** #
def on_mqtt_message(client, userdata, message):
    message = message.payload.decode()
    message = message.strip()
    logging.debug(f"Control: {message}")

    commandFields = message.split(":")
    deviceName = commandFields[0]
    commandType = commandFields[1]
    commandOptions = commandFields[2:]

    print(commandOptions)
    robotDevices[deviceName].command(commandType, commandOptions)



def setupMQTTClient():
    mqttClient = mqtt.Client()
    mqttClient.connect("localhost", 1883)
    mqttClient.subscribe("control")
    mqttClient.on_message = on_mqtt_message
    return mqttClient

def setupRobotDevices():
    global robotDevices
    leftTread = TreadMotor(motorAPI=motorKit.motor3, name="left")
    rightTread = TreadMotor(motorAPI=motorKit.motor4, name="right")
    targetingLaser = TargetingLaser()
    turretRotate = JoxServo(name="TurretRotate", gpio_pin=12)
    gunElevator = GunElevator(gpio_pin=13)
    ammoRammer = AmmoRammer(gpio_pin=16)

    robotDevices["leftTread"] = leftTread
    robotDevices["rightTread"] = rightTread
    robotDevices["targetingLaser"] = targetingLaser
    robotDevices["turretRotate"] = turretRotate
    robotDevices["gunElevator"] = gunElevator
    robotDevices["ammoRammer"] = ammoRammer

    return robotDevices




if __name__ == "__main__":
    global robotDevices
    robotDevices = {}

    FORMAT = '%(asctime)s.%(msecs)03d;%(levelname)s;%(name)s:%(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt='%H:%M:%S')

    logging.info("Log started")

    motorKit = MotorKit(i2c=board.I2C())

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

