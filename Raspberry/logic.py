import time
import connection_manager

connection_manager.mqtt_connect()

while True:
	time.sleep(5)
	print(connection_manager.get_last_message())