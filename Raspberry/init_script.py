import subprocess

import database_manager

#popola database se vuoto (con info sulla stanza di default accoppiata al sensore del raspberry)
db = database_manager.database_manager()

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

# Raspberry config
# subprocess.Popen(['python', '/home/pi/Documents/Raspberry-Thermostat/Raspberry/logic.py'])
# subprocess.Popen(['python', '/home/pi/Documents/Raspberry-Thermostat/Raspberry/sensor.py'])

# TODO: Comment/Uncomment device dependent paths
# Sem PC config
# subprocess.Popen(['python', '/home/sem/OneDrive/Politecnico di Torino/01 - Magistrale/Anno 1 -- 2018-2019/Secondo Semestre/Projects and Laboratory on Communicatons Systems/Labs/Raspberry-Thermostat/Raspberry/logic.py'])
# subprocess.Popen(['python2.7', '/home/sem/OneDrive/Politecnico di Torino/01 - Magistrale/Anno 1 -- 2018-2019/Secondo Semestre/Projects and Laboratory on Communicatons Systems/Labs/Raspberry-Thermostat/Raspberry/sensor.py'])
