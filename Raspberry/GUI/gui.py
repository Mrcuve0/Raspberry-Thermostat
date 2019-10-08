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

import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

print(sys.path[0])  # <->/Raspberry-Thermostat/Raspberry/GUI
# sys.path.insert(0, sys.path[0] + "/../../") # /Raspberry-Thermostat/
sys.path.append(sys.path[0] + "/../../")
sys.path.append(sys.path[0] + "/../")
sys.path.append("/home/pi/.local/lib/python3.5/site-packages")
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
print(sys.path)

import mainWindow
import BlankBGWindow
import init_script

from database_manager import database_manager

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

# Importa classe definita con QTDesigner
# from mainWindow import Ui_MainWindow


class MainWindow(QMainWindow, mainWindow.Ui_MainWindow):

    def __init__(self, db, actualRoomIndex):
        super(self.__class__, self).__init__()
        self.setupUi(self, db, actualRoomIndex)
        # self.initDB(db)


class BlankWindow(QMainWindow, BlankBGWindow.Ui_BlankWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


def main():
    db = database_manager()
    app = QtWidgets.QApplication(sys.argv)
    blank = BlankWindow()
    blank.showMaximized()
    raspyGUI = MainWindow(db, 0)
    raspyGUI.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
