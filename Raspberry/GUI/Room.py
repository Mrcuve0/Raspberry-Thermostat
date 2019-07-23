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

from Sensor import Sensor
from Actuator import Actuator

class Room(object):

    ID = 0

    def __init__(self):
        self.ID = self.ID + 1

        # Dizionario di sensori connessi a questa stanza
        self.sensorsDict = {}   

        # Dizionario di attuatori connessi a questa stanza
        self.actuatorsDict = {}

    ### SETTERS ###

    def addActuator(self):
        act = Actuator()
        self.actuatorsDict[act.getID()] = act

    def addSensor(self, isConnected):
        sens = Sensor(isConnected)
        self.sensorsDict[sens.getID()] = sens

    ### GETTERS ###

    def getSensorsConnected(self):
        return self.sensorsDict

    def getActuatorsConnected(self):
        return self.actuatorsDict


    

