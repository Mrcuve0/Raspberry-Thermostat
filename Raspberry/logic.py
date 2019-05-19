import time
import connection_manager
import db_manager

mqtt_manager = connection_manager.get_instance() 
mqtt_manager.mqtt_connect()

while True:
	time.sleep(5)
	last_msg = mqtt_manager.get_last_temperatures()
	print(last_msg)
	#result = db_manager.insert_log({'msg': last_msg})
	#print(result)