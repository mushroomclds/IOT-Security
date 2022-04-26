import paho.mqtt.publish as publish
import time

while True:
	print("Sending 0...")
	publish.single("ledStatus", "0", hostname="mushroom", 
		auth={'username':"mushroom", 'password':"1234"})
	time.sleep(1)
	print("Sending 1...")
	publish.single("ledStatus", "1", hostname="mushroom",
		auth={'username':"mushroom", 'password':"1234"})
	time.sleep(1)
'''
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp/ultrasonic")

import paho.mqtt.client as mqtt

MQTT_ADDRESS = '192.168.0.180'
MQTT_USER = 'mushroom'
MQTT_PASSWORD = '1234'
MQTT_TOPIC = 'esp/ultrasonic'


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))


def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()'''

