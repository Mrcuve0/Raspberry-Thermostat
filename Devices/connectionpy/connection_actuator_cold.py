# Copyright (C) 2019 Paolo Calao, Samuele Yves Cerini, Federico Pozzana


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
      if actuatorID + "group01" == recName:
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

def sendname(BTsocket, roomName):
  BTsocket.send(str(roomName))
  time.sleep(1)

def disconnect(BTsocket):
  BTsocket.close()


#############################################################################


def connection(actuatorID, roomID, net_SSID, net_PWD):
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
        sendname(BTsocket, str("roomName") + str(roomID))
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
