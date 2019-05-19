import time
import connection_manager
import db_manager

# Room settings constants
manual_settings = 'manual'
antifreeze_settings = 'antifreeze'
# Actuator constants
actuator_hot = 'hot'
actuator_hot_topic = 'actuator/hot'
actuator_cold = 'cold'
actuator_cold_topic = 'actuator/cold'
# Power constants
power_on = 'on'
power_off = 'off'

# Start mqtt connection
mqtt_manager = connection_manager.get_instance() 
mqtt_manager.mqtt_connect()

# Get last temperatures received through mqtt
last_temperatures = mqtt_manager.get_last_temperatures()
# Get configuration from the db
configuration = {'rooms_settings': [{'room': 'stanzetta', 'mode': 'manual', 'info': 25}], 'backup_config': 'none'}

def find_room_in_list(room, room_list):
	result = None
	for temp_room in room_list:
		if temp_room['room'] == room:
			result = temp_room
	return result

def drive_actuator(room, actuator_type, power):
	topic = ''
	if (actuator_type == actuator_hot):
		topic = actuator_hot_topic
	elif (actuator_type == actuator_cold):
		topic = actuator_cold_topic
	msg = str({'room': room, 'power': power})
	mqtt_manager.mqtt_publish(topic, msg)

while True:
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
			temp_temperature = temp_elem['temperature']
			if (room_settings['mode'] == manual_settings):
				if temp_temperature < room_settings['info']:
					# Enable the hot-actuator
					drive_actuator(temp_room, actuator_hot, power_on)
					drive_actuator(temp_room, actuator_cold, power_off)
				elif temp_temperature > room_settings['info']:
					drive_actuator(temp_room, actuator_hot, power_off)
					drive_actuator(temp_room, actuator_cold, power_on)
			elif (room_settings['mode'] == antifreeze_settings):
				if temp_temperature < room_settings['info']:
					# Enable the hot-actuator
					drive_actuator(temp_room, actuator_hot, power_on)
				else:
					drive_actuator(temp_room, actuator_hot, power_off)
	time.sleep(10)
	last_temperatures = mqtt_manager.get_last_temperatures()
	#result = db_manager.insert_log({'msg': last_msg})
	#print(result)