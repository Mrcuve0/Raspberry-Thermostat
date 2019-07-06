import time
import connection_manager
import db_manager
import json

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

# Define callbacks for MQTT client
def on_connect(self, client, userdata, flags, rc):
    print('Connected with result code {0}'.format(rc))
    # Subscribe (or renew if reconnect).
    client.subscribe(self.temperature_topic)

def on_message(self, client, userdata, msg):
    last_temperatures = db_manager.get_last_temperatures()
    self.last_msg = msg.payload
    #print(msg.topic+" "+str(msg.payload))
    if (msg.topic == self.temperature_topic):
        # Insert log in the database
        # Update the corresponding entry in the last temperatures structure
        room_found = False
        payload = ast.literal_eval(msg.payload)
        room_name = payload['room']
        new_temp = payload['temperature']
        for entry in last_temperatures:
            if entry['room'] == room_name:
                entry['temperature'] = new_temp
                room_found = True
        if (not room_found):
            #update_temperatures_struct from db
            new_entry = {'room': room_name, 'temperature': new_temp}
            print(new_entry)
            last_temperatures.append(new_entry)
        db_manager.update_last_temperatures(last_temperatures)
        log = {'type': 'temperature', 'room': room_name, 'val': new_temp, 'timestamp': millis()}
        db_manager.insert_log(log)

# Start mqtt connection
mqtt_manager = connection_manager()
mqtt_manager.mqtt_connect(on_connect, on_message)
# Define db manager
db_manager = database_manager()

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
	msg = json.dumps({'room': room, 'power': power})
	mqtt_manager.mqtt_publish(topic, msg)

while True:
	# Get last temperatures received through mqtt
	last_temperatures = db_manager.get_last_temperatures()
	# Get configuration from the db
	configuration = db_manager.get_configuration()
	#configuration = {'rooms_settings': [{'room': 'stanzetta', 'mode': 'manual', 'info': 25, 'extra': 'weekend'}], 'backup_config': 'none'}

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
