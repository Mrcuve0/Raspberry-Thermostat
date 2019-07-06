import sys
import time
import Adafruit_DHT
import constants

sensor = 22
pin = 4
mqtt_manager = connection_manager()
mqtt_manager.mqtt_connect()
raspberry_room = 'default' 

while(True)
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		msg = {'room': raspberry_room, 'temperature': temperature}
		mqtt_manager.mqtt_publish(temperature_topic, msg)
	time.sleep(30)