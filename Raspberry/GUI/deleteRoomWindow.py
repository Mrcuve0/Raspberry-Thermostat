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

import sys
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import settingsWindow
from database_manager import database_manager

class MyQLineEdit(QtWidgets.QLineEdit):
    def focusInEvent(self, e):
        try:
            subprocess.Popen(["dbus-send", "--type=method_call", "--print-reply", "--dest=org.onboard.Onboard", "/org/onboard/Onboard/Keyboard", "org.onboard.Onboard.Keyboard.Show"])
        except FileNotFoundError:
            pass
        super(MyQLineEdit, self).focusInEvent(e)

    def focusOutEvent(self, e):
        subprocess.Popen(["dbus-send", "--type=method_call", "--print-reply", "--dest=org.onboard.Onboard", "/org/onboard/Onboard/Keyboard", "org.onboard.Onboard.Keyboard.Hide"])
        super(MyQLineEdit, self).focusOutEvent(e)


class Ui_deleteRoomWindow(object):

    db = None
    configuration = None
    newConfiguration = None
    roomDataConfiguration = None

    actualNumRooms = 0

    def initDB(self, db):
        self.db = db

    def reloadRoomData(self):
        self.configuration = database_manager.get_configuration(self.db)
        self.roomDataConfiguration = database_manager.get_roomData_configuration(self.db)
        self.actuatorsConfiguration = database_manager.get_actuators_configuration(self.db)

    def on_PB_goBack_clicked(self):
        self.close()
        self.roomWindow = QtWidgets.QMainWindow()
        self.uiSettingsWindow = settingsWindow.Ui_SettingsWindow()
        self.uiSettingsWindow.setupUi(self.roomWindow, self.db)
        self.roomWindow.showMaximized()

    def on_PB_deleteRoom_clicked(self):
        self.actualNumRooms = len(self.configuration["rooms_settings"])
        roomName = self.LE_room.text()
        if (roomName == ""):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Room name cannot be empty")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        if (roomName.lower() == "default"):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Error! You cannot delete the main room!")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        flag = 0
        for i in range(0, self.actualNumRooms): 
            if (str(roomName).lower() == str(self.configuration["rooms_settings"][i]["room_name"]).lower()):
                if (str(roomName).lower() == str(self.roomDataConfiguration["conf"][i]["roomName"]).lower()):

                    # Se ci sono valvole associate, elimina la valvola utilizzata rendendola libera per altre stanze
                    actualNumActuators = len(self.roomDataConfiguration["conf"][i]["actuators"])
                    for j in range(0, actualNumActuators):  # Cicla sugli attatori disponibili per questa stanza
                        actualNumValves = len(self.roomDataConfiguration["conf"][i]["actuators"][j]["valves"])
                        actualNumValves_actuatorsConfig = actualNumValves
                        for k in range(0, actualNumValves): # Cicla sulle valvole disponibili per questo attuatore
                            # if (k < actualNumValves_actuatorsConfig):
                            if (str(self.roomDataConfiguration["conf"][i]["actuators"][j]["valves"][k]["valveID"]) != "" and str(self.roomDataConfiguration["conf"][i]["actuators"][j]["type"]) == "hot"):
                                # Questa valvola è collegata, togliamola da actuatorsConfiguration perché è tornata libera
                                connectedValveID = self.roomDataConfiguration["conf"][i]["actuators"][j]["valves"][k]["valveID"]
                                connectedActuatorID = self.roomDataConfiguration["conf"][i]["actuators"][j]["actuatorID"]
                                
                                actualNumActuators_actuatorsConfig = len(self.actuatorsConfiguration["conf"])
                                for l in range(0, actualNumActuators_actuatorsConfig): # Cicla sugli attuatori disponibili nella actuatorsConfiguration
                                    if (str(self.actuatorsConfiguration["conf"][l]["actuatorID"]) == connectedActuatorID):
                                        actualNumValves_actuatorsConfig = len(self.actuatorsConfiguration["conf"][l]["valves"])
                                        for m in range(0, actualNumValves_actuatorsConfig):
                                            if (m < len(self.actuatorsConfiguration["conf"][l]["valves"])):
                                                if (str(self.actuatorsConfiguration["conf"][l]["valves"][m]["valveID"]) == connectedValveID):
                                                    # self.actuatorsConfiguration["conf"][l]["valves"][m]["valveID"] = "" # Imposta la valvola come libera
                                                    del self.actuatorsConfiguration["conf"][l]["valves"][m]
                                                    actualNumValves_actuatorsConfig = actualNumValves_actuatorsConfig - 1
                                                    # actualNumValves = actualNumValves - 1
                                                    if (len(self.actuatorsConfiguration["conf"][l]["valves"]) == 0):
                                                        self.actuatorsConfiguration["conf"][l]["valves"].append({"valveID" : ""})

                    del self.configuration["rooms_settings"][i]
                    if (len(self.configuration["rooms_settings"]) == 0):
                        self.configuration["rooms_settings"].append({'room': "0", 'room_name': 'default', 'mode': 'manual', 'info': {'temp': 25, 'weekend': 0}, 'season': 'hot', "program" : {"MFM" : "", "MFE" : "", "MFN" : "", "WEM" : "", "WEE" : "", "WEN" : ""}})
                    del self.roomDataConfiguration["conf"][i]
                    if (len(self.roomDataConfiguration["conf"]) == 0):
                        self.roomDataConfiguration["conf"].append({"roomID" : "0", "roomName" : "default",  "sensors" : [{"sensorID" : ""}], "actuators" : [{"actuatorID" : "", "type" : "hot", "valves" : [{"valveID": ""}]}]})
                    flag = 1

                    break

        if (flag == 1):
            self.newConfiguration = self.configuration
            database_manager.update_configuration(self.db, self.newConfiguration)
            database_manager.update_roomData_configuration(self.db, self.roomDataConfiguration)
            database_manager.update_actuators_configuration(self.db, self.actuatorsConfiguration)

            print("\t --> COMMIT: Stanza rimossa")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setInformativeText(
                "Room deleted!\nYou will no more receive data from the related sensor. Disconnect it.")
            msg.setWindowTitle("Info")
            msg.exec_()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Error! Room not found!")
            msg.setWindowTitle("Error")
            msg.exec_()

          
    def __handleTextChanged(self, text):
        if not self.LE_room.hasFocus:
            self.LE_room._beforeRoomName = text

    def __handleEditingFinished(self):
        beforeRoomName, afterRoomName = self.LE_room._beforeRoomName, self.LE_room.text()
        if beforeRoomName != afterRoomName:
            self.LE_room._beforeRoomName = afterRoomName
            self.LE_room.textChanged.emit(afterRoomName)
            self.PB_deleteRoom.setText(QtCore.QCoreApplication.translate(
                "DeleteRoomWindow", "Delete Room"))
            self.PB_deleteRoom.setEnabled(True)
        
    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_deleteRoom.clicked.connect(self.on_PB_deleteRoom_clicked)
        self.LE_room.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)

        self.reloadRoomData()

    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def close(self):
        self.timer.stop()
        self.roomWindow.close()

    def setupUi(self, deleteRoomWindow, db):
        self.roomWindow = deleteRoomWindow
        self.roomWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        deleteRoomWindow.setObjectName("DeleteRoomWindow")
        deleteRoomWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(10)
        deleteRoomWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(deleteRoomWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(120, 0, 571, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)

        # Date and Time widgets
        self.dateEdit.setFont(font)
        self.dateEdit.setInputMethodHints(QtCore.Qt.ImhDate)
        self.dateEdit.setWrapping(False)
        self.dateEdit.setFrame(False)
        self.dateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dateEdit.setReadOnly(True)
        self.dateEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dateEdit.setObjectName("dateEdit")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(687, 0, 121, 61))

        self.timer = QTimer()

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
        
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        
        self.PB_goBack = QtWidgets.QPushButton(self.centralwidget)
        self.PB_goBack.setGeometry(QtCore.QRect(0, 380, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_goBack.setFont(font)
        self.PB_goBack.setObjectName("PB_goBack")
        self.LE_room = MyQLineEdit(self.centralwidget)
        self.LE_room.setGeometry(QtCore.QRect(110, 130, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LE_room.setFont(font)
        self.LE_room.setObjectName("LE_room")

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

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
        self.label_RoomName.setGeometry(QtCore.QRect(90, 80, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_RoomName.setFont(font)
        self.label_RoomName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_RoomName.setObjectName("label_RoomName")

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.PB_deleteRoom = QtWidgets.QPushButton(self.centralwidget)
        self.PB_deleteRoom.setGeometry(QtCore.QRect(220, 240, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_deleteRoom.setFont(font)
        self.PB_deleteRoom.setObjectName("PB_deleteRoom")
        deleteRoomWindow.setCentralWidget(self.centralwidget)

        self.initDB(db)

        self.activeFunctionsConnection()
        self.retranslateUi(deleteRoomWindow)

    def retranslateUi(self, deleteRoomWindow):
        _translate = QtCore.QCoreApplication.translate
        deleteRoomWindow.setWindowTitle(
            _translate("DeleteRoomWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(
            _translate("DeleteRoomWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate(
            "DeleteRoomWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("DeleteRoomWindow", "<"))
        self.LE_room.setPlaceholderText(_translate(
            "DeleteRoomWindow", "Insert room name"))

        self.label_RoomSettings.setText(_translate("DeleteRoomWindow", "Room\n"
                                                   "Settings"))
        self.label_RoomName.setText(_translate(
            "DeleteRoomWindow", "Room Name:"))

        self.PB_deleteRoom.setText(_translate(
            "DeleteRoomWindow", "Delete Room..."))
