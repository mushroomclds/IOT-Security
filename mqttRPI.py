import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import RPi.GPIO as GPIO
from pygame import mixer

mixer.init() #initialize mixer obj
sound = mixer.Sound('jazz.wav')#load jazz song


MQTT_ADDRESS = '192.168.0.240' #server running here 
MQTT_USER = 'mushroom'
MQTT_PASSWORD = '1234'
MQTT_TOPIC = 'esp/ultrasonic'


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)
   # client.subscribe("ledStatus")

def on_message(client, userdata, msg):
	
	distance = float(str(msg.payload)[2:-1])
	print(msg.topic + ' ' + str(distance) )
	#mixer.set_endevent()
	if not mixer.get_busy():
		if distance < 15.0:
			publish.single("ledStatus", "1", hostname="192.168.0.240")
			sound.play(1, maxtime=15000)
	elif distance > 15.0:
		mixer.stop()
		publish.single("ledStatus", "0", hostname="192.168.0.240")

def main():
	mqtt_client = mqtt.Client()
	#mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
	mqtt_client.on_connect = on_connect
	mqtt_client.on_message = on_message
	mqtt_client.connect(MQTT_ADDRESS, 1883)
	mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()


