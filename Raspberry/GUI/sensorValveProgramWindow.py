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
from PyQt5.QtCore import QTime, QDate, QTimer

import mainWindow
import sensorSettingsWindow
import valveSettingsWindow
import programSettingsWindow
import acSettingsWindow
from database_manager import database_manager


class Ui_SensorValveProgramWindow(object):

    db = None
    actualRoomIndex = 0
    actualRoomID = 0
    actualRoomName = ""

    def initDB(self, db):
        self.db = db

    def searchActualRoomID(self):
        self.configuration = database_manager.get_configuration(self.db)

        self.actualRoomID = self.configuration["rooms_settings"][self.actualRoomIndex]["room"]

    def on_PB_sensor_clicked(self):
        self.close()
        self.sensorValveProgramWindow = QtWidgets.QMainWindow()
        self.uiSensorSettingsWindow = sensorSettingsWindow.Ui_SensorSettingsWindow()
        self.uiSensorSettingsWindow.setupUi(self.sensorValveProgramWindow, self.db, self.actualRoomIndex, self.actualRoomName)
        self.sensorValveProgramWindow.showMaximized()

    def on_PB_valve_clicked(self):
        self.close()
        self.sensorValveProgramWindow = QtWidgets.QMainWindow()
        self.uiValveSettingsWindow = valveSettingsWindow.Ui_ValveSettingsWindow()
        self.uiValveSettingsWindow.setupUi(self.sensorValveProgramWindow, self.db, self.actualRoomIndex, self.actualRoomName)
        self.sensorValveProgramWindow.showMaximized()

    def on_PB_airConditioner_clicked(self):
        self.close()
        self.sensorValveProgramWindow = QtWidgets.QMainWindow()
        self.uiACSettingsWindow = acSettingsWindow.Ui_ACSettingsWindow()
        self.uiACSettingsWindow.setupUi(self.sensorValveProgramWindow, self.db, self.actualRoomIndex, self.actualRoomName)
        self.sensorValveProgramWindow.showMaximized()

    def on_PB_program_clicked(self):
        self.close()
        self.sensorValveProgramWindow = QtWidgets.QMainWindow()
        self.uiProgramSettingsWindow = programSettingsWindow.Ui_ProgramSettingsWindow()
        self.uiProgramSettingsWindow.setupUi(self.sensorValveProgramWindow, self.db, self.actualRoomIndex, self.actualRoomName)
        self.sensorValveProgramWindow.showMaximized()

    def on_PB_goBack_clicked(self):
        self.close()
        self.sensorValveProgramWindow = QtWidgets.QMainWindow()
        self.uiMainWindow = mainWindow.Ui_MainWindow()
        self.uiMainWindow.setupUi(self.sensorValveProgramWindow, self.db, self.actualRoomIndex)
        self.sensorValveProgramWindow.showMaximized()

    def activeFunctionsConnection(self):
        self.PB_sensor.clicked.connect(self.on_PB_sensor_clicked)
        self.PB_valve.clicked.connect(self.on_PB_valve_clicked)
        self.PB_timeProgram.clicked.connect(self.on_PB_program_clicked)
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_airConditioner.clicked.connect(self.on_PB_airConditioner_clicked)

        # Timer for data and time
        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)


    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def close(self):
        self.timer.stop()
        self.sensorValveProgramWindow.close()

    def setupUi(self, SensorValveProgramWindow, db, actualRoomIndex, actualRoomName):

        self.sensorValveProgramWindow = SensorValveProgramWindow
        self.sensorValveProgramWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        SensorValveProgramWindow.setObjectName("SensorValveProgramWindow")
        SensorValveProgramWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(10)
        SensorValveProgramWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(SensorValveProgramWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(687, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.timeEdit.setFont(font)
        self.timeEdit.setWrapping(False)
        self.timeEdit.setFrame(False)
        self.timeEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.timeEdit.setReadOnly(True)
        self.timeEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.timeEdit.setObjectName("timeEdit")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(120, 0, 571, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.dateEdit.setFont(font)
        self.dateEdit.setInputMethodHints(QtCore.Qt.ImhDate)
        self.dateEdit.setWrapping(False)
        self.dateEdit.setFrame(False)
        self.dateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dateEdit.setReadOnly(True)
        self.dateEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dateEdit.setObjectName("dateEdit")
        self.PB_goBack = QtWidgets.QPushButton(self.centralwidget)
        self.PB_goBack.setGeometry(QtCore.QRect(0, 380, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_goBack.setFont(font)
        self.PB_goBack.setObjectName("PB_goBack")
        self.label_RoomSettings = QtWidgets.QLabel(self.centralwidget)
        self.label_RoomSettings.setGeometry(QtCore.QRect(-10, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_RoomSettings.setFont(font)
        self.label_RoomSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_RoomSettings.setObjectName("label_RoomSettings")
        self.label_RoomName = QtWidgets.QLabel(self.centralwidget)
        self.label_RoomName.setGeometry(QtCore.QRect(200, 80, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_RoomName.setFont(font)
        self.label_RoomName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_RoomName.setObjectName("label_RoomName")
        self.PB_sensor = QtWidgets.QPushButton(self.centralwidget)
        self.PB_sensor.setGeometry(QtCore.QRect(20, 160, 181, 151))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_sensor.setFont(font)
        self.PB_sensor.setObjectName("PB_sensor")
        self.PB_valve = QtWidgets.QPushButton(self.centralwidget)
        self.PB_valve.setGeometry(QtCore.QRect(210, 160, 181, 151))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_valve.setFont(font)
        self.PB_valve.setObjectName("PB_valve")
        self.PB_timeProgram = QtWidgets.QPushButton(self.centralwidget)
        self.PB_timeProgram.setGeometry(QtCore.QRect(590, 160, 181, 151))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_timeProgram.setFont(font)
        self.PB_timeProgram.setObjectName("PB_timeProgram")
        self.PB_airConditioner = QtWidgets.QPushButton(self.centralwidget)
        self.PB_airConditioner.setGeometry(QtCore.QRect(400, 160, 181, 151))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_airConditioner.setFont(font)
        self.PB_airConditioner.setObjectName("PB_airConditioner")
        SensorValveProgramWindow.setCentralWidget(self.centralwidget)

        self.initDB(db)
        self.actualRoomIndex = actualRoomIndex
        self.actualRoomName = actualRoomName
        self.searchActualRoomID()

        self.timer = QTimer()

        self.activeFunctionsConnection()

        self.retranslateUi(SensorValveProgramWindow)

    def retranslateUi(self, SensorValveProgramWindow):

        _translate = QtCore.QCoreApplication.translate
        SensorValveProgramWindow.setWindowTitle(_translate("SensorValveProgramWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(_translate("SensorValveProgramWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate("SensorValveProgramWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("SensorValveProgramWindow", "<"))
        self.label_RoomSettings.setText(_translate("SensorValveProgramWindow", "Room\n"
"Settings"))
        self.label_RoomName.setText(_translate("SensorValveProgramWindow", "Actual Room: " + str(self.actualRoomName)))
        self.PB_sensor.setText(_translate("SensorValveProgramWindow", "Set\n"
"Sensor"))
        self.PB_valve.setText(_translate("SensorValveProgramWindow", "Set\n"
"Valves"))
        self.PB_timeProgram.setText(_translate("SensorValveProgramWindow", "Set\n"
"Program"))
        self.PB_airConditioner.setText(_translate("SensorValveProgramWindow", "Set\n"
"AirConditioner"))
