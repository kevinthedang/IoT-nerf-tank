#!/usr/bin/python3

import logging
from time import sleep
from TargetingLaser import TargetingLaser
from TreadMotor import TreadMotor

import board
from adafruit_motorkit import MotorKit
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


#Global handles to hardware objects

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


if __name__ == "__main__":
    global robotDevices
    robotDevices = {}

    FORMAT = '%(asctime)s.%(msecs)03d;%(levelname)s;%(name)s:%(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt='%H:%M:%S')

    logging.info("Log started")

    motorKit = MotorKit(i2c=board.I2C())

    leftTread = TreadMotor(motorAPI=motorKit.motor3, name="left")
    rightTread = TreadMotor(motorAPI=motorKit.motor4, name="right")
    targetingLaser = TargetingLaser()

    robotDevices["leftTread"] = leftTread
    robotDevices["rightTread"] = rightTread
    robotDevices["targetingLaser"] = targetingLaser

    mqttClient = setupMQTTClient()


    try:
        mqttClient.loop_forever()
    except KeyboardInterrupt:
        logging.info("Received keyboard interrupt - quitting.")
    finally:
        mqttClient.disconnect()

        robotDevices["leftTread"].stop()
        robotDevices["rightTread"].stop()

    logging.info("Done.")

