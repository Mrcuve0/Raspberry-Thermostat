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

class Sensor(object):

    ID = 0

    def __init__(self, isConnected):
        self.ID = self.ID + 1
        self.isConnected = isConnected

    ### SETTERS ###

    def setIsConnect(self, isConnected):
        self.isConnected = isConnected

    ### GETTERS ###

    def getID(self):
        return self.ID

    def getIsConnected(self):
        return self.isConnected
