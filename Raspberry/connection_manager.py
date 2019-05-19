import paho.mqtt.client as mqtt
import ast

class connection_manager:   
    temperature_topic = 'logs'
    actuator_topic = 'actuators'
    last_temperatures = {}
    last_msg = ""
    # Mqtt broker will run on the raspberry, so the address to use will be 'localhost'
    MQTT_SERVER = '192.168.43.154' #'localhost'
    mqtt_client = mqtt.Client()

    def __init__(self):
        self.last_temperatures = [{'room': 'default', 'temperature': 0}]

    def get_last_message(self):
        return self.last_msg

    def get_last_temperatures(self):
        return self.last_temperatures

    def mqtt_publish(self, topic, msg):
        self.mqtt_client.publish(topic, msg)

    def mqtt_publish_actuators(self, msg):
        self.mqtt_client.publish(self.actuator_topic, msg)        

    def mqtt_connect(self):
        self.mqtt_client.on_connect = self.on_connect  # Specify on_connect callback
        self.mqtt_client.on_message = self.on_message  # Specify on_message callback
        self.mqtt_client.connect(self.MQTT_SERVER, 1883, 60)  # Connect to MQTT broker (also running on Pi).
        # Start connection loop in a separate thread
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code {0}'.format(rc))
        # Subscribe (or renew if reconnect).
        client.subscribe(self.temperature_topic)

    def on_message(self, client, userdata, msg):
        self.last_msg = msg.payload
        #print(msg.topic+" "+str(msg.payload))
        if (msg.topic == self.temperature_topic):
            # Insert log in the database
            # Update the corresponding entry in the last temperatures structure
            room_found = False
            payload = ast.literal_eval(msg.payload)
            room_name = payload['room']
            new_temp = payload['temperature']
            for entry in self.last_temperatures:
                if entry['room'] == room_name:
                    entry['temperature'] = new_temp
                    room_found = True
            if (not room_found):
                #update_temperatures_struct from db
                new_entry = {'room': room_name, 'temperature': new_temp}
                print(new_entry)
                self.last_temperatures.append(new_entry)

# Implement a singleton class
connection_manager_instance = connection_manager()
def get_instance():
    return connection_manager_instance

# Callback fires when conected to MQTT broker.
def on_connect(client, userdata, flags, rc):
    connection_manager_instance.on_connect(client, userdata, flags, rc)

# Callback fires when a published message is received.
def on_message(client, userdata, msg):
    connection_manager_instance.on_message(client, userdata, msg)
