import sys
import time
import Adafruit_DHT
import constants
from connection_manager import *
import json

sensor = 22
pin = 4
mqtt_manager = connection_manager()
mqtt_manager.mqtt_connect()
raspberry_room = "0" 

while(True):
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		msg = msg = json.dumps({'room': raspberry_room, 'temperature': temperature})
		mqtt_manager.mqtt_publish(constants.temperature_topic, msg)
	time.sleep(30)