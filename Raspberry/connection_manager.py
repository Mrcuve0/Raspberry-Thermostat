import paho.mqtt.client as mqtt
import ast
import constants

class connection_manager:   
    # Mqtt broker will run on the raspberry, so the address to use will be 'localhost'
    MQTT_SERVER = 'localhost'
    MQTT_PORT = 1883
    #mqtt_client = mqtt.Client()
    mqtt_client = None
    #on_connect_callback = None
    #on_message_callback = None

    def __init__(self):
        self.mqtt_client = mqtt.Client()

    def mqtt_publish(self, topic, msg):
        self.mqtt_client.publish(topic, msg)

    def mqtt_publish_actuators(self, msg):
        self.mqtt_client.publish(constants.actuator_topic, msg)        

    def mqtt_connect(self, on_conn = None, on_mess = None):
        if on_conn is not None:
            self.mqtt_client.on_connect = on_conn
        if on_mess is not None:
            self.mqtt_client.on_message = on_mess
        self.mqtt_client.connect(self.MQTT_SERVER, self.MQTT_PORT, 60)  # Connect to MQTT broker (also running on Pi).
        # Start connection loop in a separate thread
        self.mqtt_client.loop_start()


# Examples of callbacks:
# def on_connect(self, client, userdata, flags, rc):
#     print('Connected with result code {0}'.format(rc))
#     # Subscribe (or renew if reconnect).
#     client.subscribe(self.temperature_topic)

# def on_message(self, client, userdata, msg):
#     self.last_msg = msg.payload
#     #print(msg.topic+" "+str(msg.payload))
#     if (msg.topic == self.temperature_topic):
#         # Insert log in the database
#         # Update the corresponding entry in the last temperatures structure
#         room_found = False
#         payload = ast.literal_eval(msg.payload)
#         room_name = payload['room']
#         new_temp = payload['temperature']
#         for entry in self.last_temperatures:
#             if entry['room'] == room_name:
#                 entry['temperature'] = new_temp
#                 room_found = True
#         if (not room_found):
#             #update_temperatures_struct from db
#             new_entry = {'room': room_name, 'temperature': new_temp}
#             print(new_entry)
#             self.last_temperatures.append(new_entry)
