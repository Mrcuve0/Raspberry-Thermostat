import time
from connection_manager import *
from database_manager import *
import json
import constants
import datetime

#variables
mqtt_manager = None
db_manager = None

# Define callbacks for MQTT client
#def on_connect(self, client, userdata, flags, rc):
def on_connect(client, userdata, flags, rc):
    #print('Connected with result code {0}'.format(rc))
    # Subscribe (or renew if reconnect).
    client.subscribe(constants.temperature_topic)

#def on_message(self, client, userdata, msg):
def on_message(client, userdata, msg):
	global db_manager
	last_temperatures = db_manager.get_last_temperatures()
	#self.last_msg = msg.payload
	#print("msg received:  " + msg.topic+" "+str(msg.payload))
	if (msg.topic == constants.temperature_topic):
		# Insert log in the database
		# Update the corresponding entry in the last temperatures structure
		room_found = False
		payload = ast.literal_eval(msg.payload)
		room_name = payload['room']
		new_temp = payload['temperature']
		new_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		for entry in last_temperatures:
			if entry['room'] == room_name:
				entry['temperature'] = new_temp
				entry['timestamp'] = new_timestamp
				room_found = True
		if (not room_found):
			#update_temperatures_struct from db
			new_entry = {'room': room_name, 'temperature': new_temp, 'timestamp': new_timestamp}
			last_temperatures.append(new_entry)
		db_manager.update_last_temperatures(last_temperatures)
		log = {'type': 'temperature', 'room': room_name, 'val': new_temp, 'timestamp': new_timestamp}
		log_db_entry = {'log' : log, 'flag': 0}
		db_manager.insert_log(log)

def find_room_in_list(room, room_list):
	result = None
	for temp_room in room_list:
		if temp_room['room'] == room:
			result = temp_room
	return result

def drive_actuator(room, actuator_type, power):
	global mqtt_manager
	topic = ''
	if (actuator_type == constants.actuator_hot):
		topic = constants.actuator_hot_topic
	elif (actuator_type == constants.actuator_cold):
		topic = constants.actuator_cold_topic
	msg = json.dumps({'room': room, 'power': power})
	mqtt_manager.mqtt_publish(topic, msg)

def programmable_time_classification(day, hour):
	day_str = 'MF'
	if day >= 6:
		day_str = 'WE'
	if hour >= 6 and hour <= 12:
		hour_str = 'M' 
	elif hour >= 13 and hour <= 23:
		hour_str = 'E' 
	elif hour >= 0 and hour <= 5:
		hour_str = 'N'
	return day_str + hour_str

def manual_mode(room, temperature, season, info):
	requested_temperature = info['temp']
	# Check weekend settings
	if info['weekend'] == 1 and datetime.datetime.now().isoweekday() >= 6:
		requested_temperature -= 2
	# If it is a cold season, hot actuators must be used 
	if season == 'cold':
		# Enable the hot-actuator
		if temperature < requested_temperature:
			drive_actuator(room, constants.actuator_hot, constants.power_on)						
		else:
			drive_actuator(room, constants.actuator_hot, constants.power_off)
	# If it is a hot season, cold actuators must be used
	elif season == 'hot':
		if temperature > requested_temperature:
			drive_actuator(room, constants.actuator_cold, constants.power_on)
		else:
			drive_actuator(room, constants.actuator_cold, constants.power_off)

def antifreeze_mode(room, temperature):
	if temperature < 15:
		# Enable the hot-actuator
		drive_actuator(room, constants.actuator_hot, constants.power_on)
	else:
		drive_actuator(room, constants.actuator_hot, constants.power_off)

def programmable_mode(room, temperature, season, program):
	day = datetime.datetime.now().isoweekday()
	hour = datetime.datetime.now().hour
	prog_time = programmable_time_classification(day, hour)
	requested_temperature = program[prog_time]
	# If it is a cold season, hot actuators must be used 
	if season == 'cold':
		# Enable the hot-actuator
		if temperature < requested_temperature:
			drive_actuator(room, constants.actuator_hot, constants.power_on)						
		else:
			drive_actuator(room, constants.actuator_hot, constants.power_off)
	# If it is a hot season, cold actuators must be used
	elif season == 'hot':
		if temperature > requested_temperature:
			drive_actuator(room, constants.actuator_cold, constants.power_on)
		else:
			drive_actuator(room, constants.actuator_cold, constants.power_off)

# Start mqtt connection
mqtt_manager = connection_manager()
mqtt_manager.mqtt_connect(on_connect, on_message)
# Define db manager
db_manager = database_manager()

while True:
	# Get last temperatures received through mqtt
	last_temperatures = db_manager.get_last_temperatures()
	# Get configuration from the db
	#configuration = {'rooms_settings': [{'room': 'stanzetta', 'room_name': 'stanzetta', 'mode': 'm/p/f', 'info': {'temp': 25, 'weekend': 0}, 'season': 'hot/cold'}], 'backup_config': 'none'}
	configuration = db_manager.get_configuration()
	# Manage only rooms from which temperatures are received since the last power-on
	#for entry in last_temperatures:
	#	temp_room = entry['room']
	#	temp_temperature = entry['temperature'] 
	#	room_settings = find_room_in_list(temp_room, configuration['rooms_settings'])
	#
	# Manage every room of the configuration
	for room_settings in configuration['rooms_settings']:
		temp_room = room_settings['room']
		temp_elem = find_room_in_list(temp_room, last_temperatures)
		if temp_elem is not None:
			# Check if the last temperature received is recent or not
			time_now = int(datetime.datetime.now().strftime("%Y%m%d%H"))
			prev_timestamp = temp_elem['timestamp']
			prev_date = datetime.datetime.strptime(prev_timestamp, "%Y-%m-%d %H:%M:%S.%f")
			prev_time = int(prev_date.strftime("%Y%m%d%H"))
			if prev_time == time_now:
				# Take the room's last temperature
				temp_temperature = temp_elem['temperature']
				temp_season = room_settings['season'] 
				temp_info = room_settings['info']
				# Manual mode
				if (room_settings['mode'] == constants.manual_settings):
					manual_mode(temp_room, temp_temperature, temp_season, temp_info)
				# Antifreeze mode
				elif (room_settings['mode'] == constants.antifreeze_settings):
					antifreeze_mode(temp_room, temp_temperature)
				# Programmable mode
				elif (room_settings['mode'] == constants.programmable_settings):
					temp_program = room_settings['program']
					programmable_mode(temp_room, temp_temperature, temp_season, temp_program)
	time.sleep(30)
