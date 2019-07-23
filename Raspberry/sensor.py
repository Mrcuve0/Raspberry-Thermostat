# Copyright (C) 2019 Paolo Calao, Samuele Yves Cerini, Federico Pozzana


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
		msg = msg = json.dumps({'room': raspberry_room, 'temperature': round(temperature, 1)})
		mqtt_manager.mqtt_publish(constants.temperature_topic, msg)
	time.sleep(30)