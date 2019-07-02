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
def connect(target_address):
  BTsocket.connect((target_address, 1))
#########################################################################
def disconnect():
  BTsocket.close()
#########################################################################
def sendIdentification():
  BTsocket.send(":termo")
  time.sleep(1)
#########################################################################
def sendCredentials():
  BTsocket.send("wifissid")
  time.sleep(1)
  BTsocket.send("wifipsw")
  time.sleep(1)
#########################################################################
def sendMQTT():
  BTsocket.send("mqttserver")
  time.sleep(1)
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
def connection():
  lookUpNearbyBluetoothDevices()
  connect(target_address)
  sendIdentification()
  receiveMessages()
  print data
  if data == '@':
    sendCredentials()
    receiveMessages()
    print data
    if data == '@':
      sendMQTT()
      receiveMessages()
      print data
      if data == '@':
        disconnect()
      else:
        disconnect()
    else:
      disconnect()
  else:
    disconnect()
#########################################################################

connection()
