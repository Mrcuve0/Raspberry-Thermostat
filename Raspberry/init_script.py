import subprocess

import database_manager

print("Chicco sono entrato nell'init")
#popola database se vuoto (con info sulla stanza di default accoppiata al sensore del raspberry)
db = database_manager.database_manager()
print("passato errore strano")
# Check and init configuration
config = db.get_configuration()
if config == None:
	config = {'rooms_settings': [{'room': 'default', 'room_name': 'default', 'mode': 'manual', 'info': {'temp': 25, 'weekend': 0}, 'season': 'hot'}], 'backup_config': 'none'}
	db.update_configuration(config)
# Check and init last_temperatures
last_t = db.get_last_temperatures()
if last_t == None:
	last_t = []
	db.update_last_temperatures(last_t)

subprocess.Popen(['python', '/home/pi/Documents/Raspberry-Thermostat/Raspberry/logic.py'])
subprocess.Popen(['python', '/home/pi/Documents/Raspberry-Thermostat/Raspberry/sensor.py'])
