import bluetooth
from bluetooth import *
import time
BTsocket=BluetoothSocket( RFCOMM )

target_name = "ESP32test"
target_address = None
data = None
#########################################################################
def receiveMessages():
  global data
  data = BTsocket.recv(1)
#########################################################################
def sendIdentification(target_address):
  BTsocket.connect((target_address, 1))
  BTsocket.send(":termo")
  time.sleep(5)
#########################################################################
def sendCredentials(target_address):
  BTsocket.send("ssid")
  time.sleep(5)
  BTsocket.send("psw")
  time.sleep(5)
#########################################################################
def sendMQTT(target_address):
  BTsocket.send("mqttserver")
  time.sleep(5)
  BTsocket.close()
#########################################################################
def lookUpNearbyBluetoothDevices():
  nearby_devices = bluetooth.discover_devices()

  for bdaddr in nearby_devices:
      if target_name == bluetooth.lookup_name( bdaddr ):
          global target_address
          target_address = bdaddr
          break

  if target_address is not None:
      print "found target bluetooth device with address ", target_address
  else:
      print "could not find target bluetooth device nearby"
#########################################################################

lookUpNearbyBluetoothDevices()
sendIdentification(target_address)
receiveMessages()
print data
if data == '@':
    sendCredentials(target_address)
    sendMQTT(target_address)
else:
    BTsocket.close()
