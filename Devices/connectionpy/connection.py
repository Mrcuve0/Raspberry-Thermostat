import bluetooth
from bluetooth import *
import time
BTsocket=BluetoothSocket( RFCOMM )

target_name = "ESP32test"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print "found target bluetooth device with address ", target_address
else:
    print "could not find target bluetooth device nearby"


BTsocket.connect((target_address, 1))

BTsocket.send(":termo")
time.sleep(5)
BTsocket.send("ssid")
time.sleep(5)
BTsocket.send("psw")
time.sleep(5)
BTsocket.close()
