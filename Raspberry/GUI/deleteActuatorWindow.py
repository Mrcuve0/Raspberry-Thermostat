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

# print(sys.path[0])  # <->/Raspberry-Thermostat/Raspberry/GUI
# sys.path.insert(0, sys.path[0] + "/../../") # /Raspberry-Thermostat/
# print(sys.path)


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import settingsWindow
from Devices.connectionpy import connection_actuator
import networkConnection
import data
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


class Ui_deleteActuatorWindow(object):

    db = None
    actuatorsConfiguration = None

    def initDB(self, db):
        self.db = db

    def on_PB_goBack_clicked(self):
        self.close()
        self.deleteActuatorWindow = QtWidgets.QMainWindow()
        self.uiSettingsWindow = settingsWindow.Ui_SettingsWindow()
        self.uiSettingsWindow.setupUi(self.deleteActuatorWindow, self.db)
        self.deleteActuatorWindow.showMaximized()

    def on_PB_deleteActuator_pressed(self):
        self.PB_deleteActuator.setText(QtCore.QCoreApplication.translate(
            "DeleteActuatorWindow", "Deleting, please wait..."))

    def on_PB_deleteActuator_released(self):
        actuatorID = self.LE_actuator.text()

        if (actuatorID == "" or not(str(actuatorID).isdecimal())):
            print("Actuator ID empty or non numerical!")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Insert a valid numerical-only ID")
            msg.setWindowTitle("Error")
            msg.exec_()

        else: # ID attuatore inserito correttamente
            # Cerca l'attuatore, se esiste eliminalo
            flag = 0
            actualNumActuators = len(self.actuatorsConfiguration["conf"])
            for i in range(0, actualNumActuators):
                if (str(actuatorID).lower() == str(self.actuatorsConfiguration["conf"][i]["actuatorID"]).lower()):
                    del self.actuatorsConfiguration["conf"][i]
                    if (len(self.actuatorsConfiguration["conf"]) == 0):
                        self.actuatorsConfiguration["conf"].append({"actuatorID" : "", "type": "cold", "valves" : [{"valveID" : ""}]})
                    flag = 1
                    break

            if (flag == 1):
                database_manager.update_actuators_configuration(self.db, self.actuatorsConfiguration)
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setInformativeText(
                    "Actuator Deleted!")
                msg.setWindowTitle("Deleted!")
                msg.exec_()

            else: # ID Attuatore non trovato, messaggio di errore
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText(
                    "ID Actuator not found!")
                msg.setWindowTitle("Error")
                msg.exec_()

        self.PB_deleteActuator.setText(QtCore.QCoreApplication.translate(
            "DeleteActuatorWindow", "Delete"))

    def reloadRoomData(self):
        self.actuatorsConfiguration = database_manager.get_actuators_configuration(self.db)

    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_deleteActuator.pressed.connect(self.on_PB_deleteActuator_pressed)
        self.PB_deleteActuator.released.connect(self.on_PB_deleteActuator_released)
        self.LE_actuator.setFocusPolicy(QtCore.Qt.StrongFocus)

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
        self.actuatorWindow.close()

    def setupUi(self, deleteActuatorWindow, db):
        self.actuatorWindow = deleteActuatorWindow
        self.actuatorWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        deleteActuatorWindow.setObjectName("DeleteActuatorWindow")
        deleteActuatorWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(10)
        deleteActuatorWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(deleteActuatorWindow)
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
        self.LE_actuator = MyQLineEdit(self.centralwidget)
        self.LE_actuator.setGeometry(QtCore.QRect(110, 130, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LE_actuator.setFont(font)
        self.LE_actuator.setObjectName("LE_actuator")

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.label_ActuatorSettings = QtWidgets.QLabel(self.centralwidget)
        self.label_ActuatorSettings.setGeometry(QtCore.QRect(-10, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_ActuatorSettings.setFont(font)
        self.label_ActuatorSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ActuatorSettings.setObjectName("label_ActuatorSettings")
        self.label_ActuatorName = QtWidgets.QLabel(self.centralwidget)
        self.label_ActuatorName.setGeometry(QtCore.QRect(90, 80, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_ActuatorName.setFont(font)
        self.label_ActuatorName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ActuatorName.setObjectName("label_ActuatorName")

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.PB_deleteActuator = QtWidgets.QPushButton(self.centralwidget)
        self.PB_deleteActuator.setGeometry(QtCore.QRect(220, 240, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_deleteActuator.setFont(font)
        self.PB_deleteActuator.setObjectName("PB_deleteActuator")
        deleteActuatorWindow.setCentralWidget(self.centralwidget)

        self.initDB(db)

        self.activeFunctionsConnection()
        self.retranslateUi(deleteActuatorWindow)
        QtCore.QMetaObject.connectSlotsByName(deleteActuatorWindow)

    def retranslateUi(self, deleteActuatorWindow):
        _translate = QtCore.QCoreApplication.translate
        deleteActuatorWindow.setWindowTitle(
            _translate("DeleteActuatorWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(
            _translate("DeleteActuatorWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate(
            "DeleteActuatorWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("DeleteActuatorWindow", "<"))
        self.LE_actuator.setPlaceholderText(_translate(
            "DeleteActuatorWindow", "Insert actuator ID"))

        self.label_ActuatorSettings.setText(_translate("DeleteActuatorWindow", "Actuator\n"
                                                   "Settings"))
        self.label_ActuatorName.setText(_translate(
            "DeleteActuatorWindow", "Actuator Name:"))

        self.PB_deleteActuator.setText(_translate(
            "DeleteActuatorWindow", "Delete"))
