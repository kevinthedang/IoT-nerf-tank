#!/usr/bin/python3
#
#   RGB LED lights strip server
#   MQTT message API
#
# Constributors:
#  Aaron S. Crandall <crandall@gonzaga.edu>
#
# Copyright 2023
#

import logging
import time


import board
import neopixel
import paho.mqtt.client as mqtt

PIXEL_STRIP_PIN = board.D21
PIXEL_LIGHTS_COUNT = 8
PIXEL_RGB_ORDER = neopixel.GRB


# ****************************************************#
def on_mqtt_message(client, userdata, message):
    message = message.payload.decode()
    message = message.strip()
    logging.debug(f"lights: {message}")

    handle_lights_message(message)


def handle_lights_message(message: str):
    global pixels
    # blankLights
    if message.startswith("blankLights"):
        blankStrip(pixels)
    # setLight:index:R:G:B
    elif message.startswith("setLight"):
        vals = message.split(":")
        index = int(vals[1])
        red = int(vals[2])
        green = int(vals[3])
        blue = int(vals[4])
        pixels[index] = (red, green, blue)
        pixels.show()
    

def blankStrip(pixels):
    pixels.fill((0,0,0,0))
    pixels.show()


def setupMQTTClient():
    mqttClient = mqtt.Client()
    mqttClient.connect("localhost", 1883)
    mqttClient.subscribe("lights")
    mqttClient.on_message = on_mqtt_message
    return mqttClient


def setupLEDStrip():
    global pixels
    pixels = neopixel.NeoPixel(
        PIXEL_STRIP_PIN, PIXEL_LIGHTS_COUNT, brightness=0.2, auto_write=False, pixel_order=PIXEL_RGB_ORDER
    )
    blankStrip(pixels)
    logging.info("LED Pixel strip connected")
    return pixels



# ********************************************************#
if __name__ == "__main__":
    global pixels

    FORMAT = '%(asctime)s.%(msecs)03d;%(levelname)s;%(name)s:%(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt='%H:%M:%S')

    setupLEDStrip()
    mqttClient = setupMQTTClient()

    logging.info("System setup - starting main loop")
    try:
        mqttClient.loop_forever()
    except KeyboardInterrupt:
        logging.info("Received interrupt - quitting")
    finally:
        mqttClient.disconnect()

    logging.info("Done.")
