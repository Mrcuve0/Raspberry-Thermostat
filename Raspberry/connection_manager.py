import paho.mqtt.client as mqtt
# Mqtt broker will run on the raspberry, so the address to use will be 'localhost'
MQTT_SERVER = '192.168.43.154' #'localhost'

last_msg = ""

	# Callback fires when conected to MQTT broker.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code {0}'.format(rc))
    # Subscribe (or renew if reconnect).
    client.subscribe('raspone')
    client.publish('raspone', 'msg')

# Callback fires when a published message is received.
def on_message(client, userdata, msg):
    global last_msg
    print(msg.topic+" "+str(msg.payload))
    last_msg = msg.payload

def get_last_message():
    return last_msg

def mqtt_connect():
    client = mqtt.Client()
    client.on_connect = on_connect  # Specify on_connect callback
    client.on_message = on_message  # Specify on_message callback
    client.connect(MQTT_SERVER, 1883, 60)  # Connect to MQTT broker (also running on Pi).
    # Start connection loop in a separate thread
    client.loop_start()
