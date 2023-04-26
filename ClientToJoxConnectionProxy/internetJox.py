"""
D Squad: Drew Bogdan, Kevin Dang, Kole Davis, Vincent Do
Description: Raspberry Pi program for tank controls using AWS connection
             to receive and execute commands
Run: python3 main.py --topic topic_1 --ca_file ~/certs/AmazonRootCA1.pem \
     --cert ~/certs/certificate.pem.crt --key ~/certs/private.pem.key --endpoint <your aws endpoint here>
"""
import command_line_utils
from uuid import uuid4
import threading
from awscrt import mqtt
import sys
import json
import paho.mqtt.client as mqtt2

from time import sleep

# Parse arguments from command line
cmd_utils = command_line_utils.CommandLineUtils("PubSub - Send and receive messages through an MQTT connection.")
cmd_utils.add_common_mqtt_commands()
cmd_utils.add_common_topic_message_commands()
cmd_utils.add_common_proxy_commands()
cmd_utils.add_common_logging_commands()
cmd_utils.register_command("key", "<path>", "Path to your key in PEM format.", True, str)
cmd_utils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", True, str)
cmd_utils.register_command("port", "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=auto).", type=int)
cmd_utils.register_command("client_id", "<str>", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))
cmd_utils.register_command("is_ci", "<str>", "If present the sample will run in CI mode (optional, default='None')")
cmd_utils.get_args()

stop_event = threading.Event()
is_ci = cmd_utils.get_command("is_ci", None) != None


def setupMQTTClient():
    # setup session with local server
    mqttClient = mqtt2.Client()
    mqttClient.connect("localhost", 1883)
    return mqttClient


# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print(f"Connection interrupted. error: {error}")


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(f"Connection resumed. return_code: {return_code} session_present: {session_present}")

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print(f"Resubscribe results: {resubscribe_results}")

        for topic, qos in resubscribe_results["topics"]:
            if qos is None:
                sys.exit(f"Server rejected resubscribe to topic: {topic}")


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print(f"Received message from topic '{topic}': {payload}")
    msg = json.loads(payload.decode("utf-8"))
    cmd = msg["command"]

    global offset
    offset = not offset

    # TURRET
    if cmd == "fire!":
        print("FIRING")
        mqttClient.publish("lights", "setPixel:1:0:0:240")
        mqttClient.publish("lights", "setPixel:2:0:0:240")
        mqttClient.publish("lights", "setPixel:3:0:0:240")
        mqttClient.publish("lights", "setPixel:4:0:0:240")
        mqttClient.publish("lights", "setPixel:5:0:0:240")
        mqttClient.publish("control", "flywheel:fire")
        sleep(4.2)
        mqttClient.publish("lights", "setPixel:1:240:0:0")
        mqttClient.publish("lights", "setPixel:2:240:0:0")
        mqttClient.publish("lights", "setPixel:3:240:0:0")
        mqttClient.publish("lights", "setPixel:4:240:0:0")
        mqttClient.publish("lights", "setPixel:5:240:0:0")
        mqttClient.publish("control", "ammoRammer:fire")
        sleep(1.0)
        mqttClient.publish("lights", "setPixel:1:0:240:0")
        mqttClient.publish("lights", "setPixel:2:0:240:0")
        mqttClient.publish("lights", "setPixel:3:0:240:0")
        mqttClient.publish("lights", "setPixel:4:0:240:0")
        mqttClient.publish("lights", "setPixel:5:0:240:0")
    elif cmd == "burst":
        print("FIRING")
        mqttClient.publish("lights", "setPixel:1:0:0:240")
        mqttClient.publish("lights", "setPixel:2:0:0:240")
        mqttClient.publish("lights", "setPixel:3:0:0:240")
        mqttClient.publish("lights", "setPixel:4:0:0:240")
        mqttClient.publish("lights", "setPixel:5:0:0:240")
        mqttClient.publish("control", "flywheel:fire")
        sleep(1)
        mqttClient.publish("lights", "setPixel:1:240:0:0")
        mqttClient.publish("lights", "setPixel:2:240:0:0")
        mqttClient.publish("lights", "setPixel:3:240:0:0")
        mqttClient.publish("lights", "setPixel:4:240:0:0")
        mqttClient.publish("lights", "setPixel:5:240:0:0")
        mqttClient.publish("control", "ammoRammer:fire")
        sleep(1)
        mqttClient.publish("control", "ammoRammer:fire")
        sleep(1)
        mqttClient.publish("control", "ammoRammer:fire")
        mqttClient.publish("lights", "setPixel:1:0:240:0")
        mqttClient.publish("lights", "setPixel:2:0:240:0")
        mqttClient.publish("lights", "setPixel:3:0:240:0")
        mqttClient.publish("lights", "setPixel:4:0:240:0")
        mqttClient.publish("lights", "setPixel:5:0:240:0")

    elif cmd == "up":
        print("UP")
        mqttClient.publish("control", "gunElevator:up:10")
    elif cmd == "down":
        print("DOWN")
        mqttClient.publish("control", "gunElevator:down:10")
    elif cmd == "r-aim":
        print("AIM RIGHT")
        mqttClient.publish("control", "turretRing:turnRight:10")
    elif cmd == "l-aim":
        print("AIM LEFT")
        mqttClient.publish("control", "turretRing:turnLeft:10")
    # TANK
    elif cmd == "right":
        print("RIGHT TURN")
        if offset:
            mqttClient.publish("control", "leftTread:drive:0.7")
            mqttClient.publish("control", "rightTread:drive:-0.7")
        else:
            mqttClient.publish("control", "leftTread:drive:0.701")
            mqttClient.publish("control", "rightTread:drive:-0.701")
    elif cmd == "left":
        print("LEFT TURN")
        if offset:
            mqttClient.publish("control", "rightTread:drive:0.7")
            mqttClient.publish("control", "leftTread:drive:-0.7")
        else:
            mqttClient.publish("control", "rightTread:drive:0.701")
            mqttClient.publish("control", "leftTread:drive:-0.701")
    elif cmd == "forward":
        print("FORWARD")
        if offset:
            mqttClient.publish("control", "leftTread:drive:1")
            mqttClient.publish("control", "rightTread:drive:1")
        else:
            mqttClient.publish("control", "leftTread:drive:0.9901")
            mqttClient.publish("control", "rightTread:drive:0.9901")
    elif cmd == "reverse":
        print("REVERSING")
        if offset:
            mqttClient.publish("control", "leftTread:drive:-1")
            mqttClient.publish("control", "rightTread:drive:-1")
        else:
            mqttClient.publish("control", "leftTread:drive:-0.9901")
            mqttClient.publish("control", "rightTread:drive:-0.9901")
    # MISC
    elif cmd == "laser-on":
        print("TURNING TARGETING LASER ON")
        mqttClient.publish("control", "targetingLaser:on")
        mqttClient.publish("lights", "setPixel:6:255:165:0")
    elif cmd == "laser-off":
        print("TURNING TARGETING LASER OFF")
        mqttClient.publish("control", "targetingLaser:off")
        mqttClient.publish("lights", "setPixel:6:0:0:0")
    elif cmd == "disconnect":
        print("DISCONNECTING FROM JOX")
        mqttClient.publish("lights", "setPixel:1:240:0:0")
        mqttClient.publish("lights", "setPixel:2:240:0:0")
        mqttClient.publish("lights", "setPixel:3:240:0:0")
        mqttClient.publish("lights", "setPixel:4:240:0:0")
        mqttClient.publish("lights", "setPixel:5:240:0:0")
        mqttClient.publish("lights", "setPixel:6:0:0:0")
        sleep(0.5)
        # instead of stopping the listening loop / disconnect this client from Jox to prevent message sending (ONLY CONNECT IF A USER IS CONNECTED TO HERE)
        mqttClient.disconnect()
        # stop_event.set()
    elif cmd == "connect":
        print("RECEIVING CONNECTION FROM OUTSIDE CLIENT")
        mqttClient.reconnect()

        # set servos back to home position on new user connect
        mqttClient.publish("control", "targetingLaser:off")
        mqttClient.publish("control", "gunElevator:setHome:")
        mqttClient.publish("control", "turretRing:setHome:")
        mqttClient.publish("lights", "setPixel:1:0:240:0")
        mqttClient.publish("lights", "setPixel:2:0:240:0")
        mqttClient.publish("lights", "setPixel:3:0:240:0")
        mqttClient.publish("lights", "setPixel:4:0:240:0")
        mqttClient.publish("lights", "setPixel:5:0:240:0")

    else:
        print("UNKNOWN COMMAND", cmd)


def main():
    mqtt_connection = cmd_utils.build_mqtt_connection(on_connection_interrupted, on_connection_resumed)

    if is_ci == False:
        print(f"Connecting to {cmd_utils.get_command(cmd_utils.m_cmd_endpoint)} with client ID '{cmd_utils.get_command('client_id')}'...")
    else:
        print("Connecting to endpoint with client ID")

    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")
    message_topic = cmd_utils.get_command(cmd_utils.m_cmd_topic)
 
    # Subscribe
    print(f"Subscribing to topic '{message_topic}'...")
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=message_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received
    )

    subscribe_result = subscribe_future.result()
    print(f"Subscribed with {str(subscribe_result['qos'])}")

    # setup local mqtt mosq server client variable and wait for aws message to connect to jox
    global mqttClient
    global offset
    mqttClient = setupMQTTClient()
    mqttClient.publish("lights", "setPixel:1:240:0:0")
    mqttClient.publish("lights", "setPixel:2:240:0:0")
    mqttClient.publish("lights", "setPixel:3:240:0:0")
    mqttClient.publish("lights", "setPixel:4:240:0:0")
    mqttClient.publish("lights", "setPixel:5:240:0:0")
    mqttClient.publish("lights", "setPixel:6:0:0:0")
    sleep(0.5)
    mqttClient.disconnect()
    offset = False

    try:
        # WAITS FOR SHUTDOWN COMMAND
        stop_event.wait()
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        print("\nManual Interruption By User...")
        mqttClient.publish("lights", "setPixel:1:0:0:0")
        mqttClient.publish("lights", "setPixel:2:0:0:0")
        mqttClient.publish("lights", "setPixel:3:0:0:0")
        mqttClient.publish("lights", "setPixel:4:0:0:0")
        mqttClient.publish("lights", "setPixel:5:0:0:0")
        mqttClient.publish("lights", "setPixel:6:0:0:0")
        sleep(0.5)
        mqttClient.disconnect()


    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    sleep(0.5)
    print("Disconnected!")


if __name__ == "__main__":
    main()
