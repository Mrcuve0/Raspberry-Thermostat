import bluetooth
from bluetooth import *
import time

import Raspberry.GUI.networkConnection

# ID dell'attuatore per prova, il vero ID viene dall'interfaccia
# target_name = "Actuator 1"
target_address = None
data = ""


def lookUpNearbyBluetoothDevices(actuatorID):
  nearby_devices = bluetooth.discover_devices()

  for bdaddr in nearby_devices:
      recName = bluetooth.lookup_name( bdaddr )
      if actuatorID == recName:
          global target_address
          target_address = bdaddr
          break

  if target_address is not None:
      print("found target bluetooth device with address " + target_address)
      return 0
  else:
      print("could not find target bluetooth device nearby")
      return -1

def connect(BTsocket, target_address):
  try:
    BTsocket.connect((target_address, 1))
    return 0
  except BluetoothError:
    disconnect(BTsocket)
    return -2
  else:
    pass

def sendIdentification(BTsocket):
  BTsocket.send(":termo")
  time.sleep(1)

def receiveMessages(BTsocket):
  global data

  try:
    data = BTsocket.recv(1)
  except BluetoothError:
    disconnect(BTsocket)
    return -3
  else:
    return 0
  
def sendssid(BTsocket, net_SSID):
  BTsocket.send(str(net_SSID))
  time.sleep(1)

def sendpsw(BTsocket, net_PWD):
  BTsocket.send(str(net_PWD))
  time.sleep(1)

def sendMQTT(BTsocket):
  BTsocket.send("mqttserver")
  time.sleep(1)

def disconnect(BTsocket):
  BTsocket.close()


#############################################################################


def connection(actuatorID, net_SSID, net_PWD):
  BTsocket = BluetoothSocket(RFCOMM)

  if (lookUpNearbyBluetoothDevices(actuatorID) == -1): # Error, device not found
    return -1

  if (connect(BTsocket, target_address) == -2): # Error, file descriptor in a bad state
    return -2

  sendIdentification(BTsocket)

  if (receiveMessages(BTsocket) == -3): # Not OK, no messages received
    return -3

  print(str(data))
  if (data == b'@'):
    sendssid(BTsocket, net_SSID)
    receiveMessages(BTsocket)
    print(data)
    if (data == b'@'):
      sendpsw(BTsocket, net_PWD)
      receiveMessages(BTsocket)
      print(data)
      if (data == b'@'):
        sendMQTT(BTsocket)
        receiveMessages(BTsocket)
        print(data)
        if (data == b'@'):
          print ("connection successful")
          disconnect(BTsocket)
          return 0
        else:
          print ("connection unsuccessful")
          disconnect(BTsocket)
          return -7
      else:
        print ("connection unsuccessful")
        disconnect(BTsocket)
        return -6
    else:
      print ("connection unsuccessful")
      disconnect(BTsocket)
      return -5
  else:
    print ("connection unsuccessful")
    disconnect(BTsocket)
    return -4


# connection()
