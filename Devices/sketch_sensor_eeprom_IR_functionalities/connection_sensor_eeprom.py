# Copyright (C) 2019 Paolo Calao, Samuele Yves Cerini, Federico Pozzana
#
#
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
BTsocket=BluetoothSocket( RFCOMM )

target_name = "Sensor 1"
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
def sendssid():
  BTsocket.send("AndroidAP")
  time.sleep(1)
#########################################################################
def sendpsw():
  BTsocket.send("diosalame")
  time.sleep(1)
#########################################################################
def sendname():
  BTsocket.send("room_name,5")
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
    sendssid()
    receiveMessages()
    print data
    if data == '@':
      sendpsw()
      receiveMessages()
      print data
      if data == '@':
        sendMQTT()
        receiveMessages()
        print data
        if data == '@':
          sendname()
          receiveMessages()
          print data
          if data == '@':
            print ("connection successful")
            disconnect()
          else:
            print ("connection unsuccessful")
            disconnect()
        else:
          print ("connection unsuccessful")
          disconnect()
      else:
        print ("connection unsuccessful")
        disconnect()
    else:
      print ("connection unsuccessful")
      disconnect()
  else:
    print ("connection unsuccessful")
    disconnect()
#########################################################################

connection()
