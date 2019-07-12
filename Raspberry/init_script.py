import subprocess

import database_manager

#popola database se vuoto (con info sulla stanza di default accoppiata al sensore del raspberry)
db = database_manager.database_manager()

# Check and init configuration
config = db.get_configuration()

# TODO: Ucomment below line to reset DB
# config = None
if config == None:
	config = {'rooms_settings': [{'room': 0, 'room_name': 'default', 'mode': 'manual', 'info': {'temp': 25, 'weekend': 0}, 'season': 'hot'}]}
	db.update_configuration(config)

# Check and init last_temperatures
last_t = db.get_last_temperatures()

# TODO: uncomment below line to reset DB
last_t = None
if last_t == None:
	last_t = []
	db.update_last_temperatures(last_t)

# Check and init roomData
roomData_config = db.get_roomData_configuration()

# TODO: Uncomment below line to reset DB
# roomData_config = None
if roomData_config == None:
	roomData_config = {"conf" : [{"roomID" : 0, "roomName" : "default",  "sensors" : {"sensorID" : ""}, "actuators" : {"actuatorID" : "", "valves" : {"valveID": ""}}}]}
	db.update_roomData_configuration(roomData_config)


# Raspberry config
# subprocess.Popen(['python', '/home/pi/Documents/Raspberry-Thermostat/Raspberry/logic.py'])
# subprocess.Popen(['python', '/home/pi/Documents/Raspberry-Thermostat/Raspberry/sensor.py'])

# TODO: Comment/Uncomment device dependent paths
# Sem PC config
# subprocess.Popen(['python', '/home/sem/OneDrive/Politecnico di Torino/01 - Magistrale/Anno 1 -- 2018-2019/Secondo Semestre/Projects and Laboratory on Communicatons Systems/Labs/Raspberry-Thermostat/Raspberry/logic.py'])
# subprocess.Popen(['python2.7', '/home/sem/OneDrive/Politecnico di Torino/01 - Magistrale/Anno 1 -- 2018-2019/Secondo Semestre/Projects and Laboratory on Communicatons Systems/Labs/Raspberry-Thermostat/Raspberry/sensor.py'])
