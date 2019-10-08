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

import subprocess

import database_manager

#popola database se vuoto (con info sulla stanza di default accoppiata al sensore del raspberry)
db = database_manager.database_manager()

# Check and init configuration
config = db.get_configuration()
# TODO: Ucomment below line to reset DB
# config = None
if config == None:
	config = {'rooms_settings': [{'room': "0", 'room_name': 'default', 'mode': 'manual', 'info': {'temp': 25, 'weekend': 0}, 'season': 'hot', "program" : {"MFM" : "", "MFE" : "", "MFN" : "", "WEM" : "", "WEE" : "", "WEN" : ""}}]}
	db.update_configuration(config)

# Check and init last_temperatures
last_t = db.get_last_temperatures()
# TODO: uncomment below line to reset DB
# last_t = None
if last_t == None:
	last_t = []
	db.update_last_temperatures(last_t)

# Check and init roomData
roomData_config = db.get_roomData_configuration()
# TODO: Uncomment below line to reset DB
# roomData_config = None
if roomData_config == None:
	roomData_config = {"conf" : [{"roomID" : "0", "roomName" : "default",  "sensors" : [{"sensorID" : "0"}], "actuators" : [{"actuatorID" : "", "type" : "hot", "valves" : [{"valveID": ""}]}]}]}
	db.update_roomData_configuration(roomData_config)

# Check and init roomData
actuators_config = db.get_actuators_configuration()
# TODO: Uncomment below line to reset DB
# actuators_config = None
if actuators_config == None:
	# actuators_config = {"conf" : [{"actuatorID" : 0, "valves" : [{"valveID": ""}]}]}
	actuators_config = {"conf" : [{"actuatorID" : "", "type": "cold", "valves" : [{"valveID" : ""}]}]}
	# actuators_config = {"conf" : [{"actuatorID" : "", "valves" : [{"valveID" : "", "linkedRoomID" : ""}]}]}
	db.update_actuators_configuration(actuators_config)

# Restart avahi-deamon
subprocess.Popen(["sudo", "systemctl", "restart", "avahi-daemon.service"])

# Raspberry config
subprocess.Popen(['python', '/home/pi/Documents/Raspberry-Thermostat/Raspberry/logic.py'])
subprocess.Popen(['python', '/home/pi/Documents/Raspberry-Thermostat/Raspberry/sensor.py'])

# TODO: Uncomment for presentation
subprocess.Popen(["python", "/home/pi/Documents/Raspberry-Thermostat/Raspberry/remote_service.py"])
