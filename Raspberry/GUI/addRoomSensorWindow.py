# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addRoomSensorWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

import sys

print(sys.path[0])  # <->/Raspberry-Thermostat/Raspberry/GUI
sys.path.insert(0, sys.path[0] + "/../../") # /Raspberry-Thermostat/
print(sys.path)

import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import mainWindow
# from Devices.connectionpy import connection
from Devices.connectionpy import connection


roomName = ""


class MyQLineEdit(QtWidgets.QLineEdit):
    def focusInEvent(self, e):
        try:
            subprocess.Popen(["onboard"])
        except FileNotFoundError:
            pass
        super(MyQLineEdit, self).focusInEvent(e)

    def focusOutEvent(self, e):
        subprocess.Popen(["killall", "onboard"])
        super(MyQLineEdit, self).focusOutEvent(e)


class Ui_AddRoomSensorWindow(object):

    def on_PB_goBack_clicked(self):
        self.close()
        self.roomWindow = QtWidgets.QMainWindow()
        self.uiMainWindow = mainWindow.Ui_MainWindow()
        self.uiMainWindow.setupUi(self.roomWindow)
        self.roomWindow.showMaximized()

    # TODO:
    def on_PB_connect_pressed(self):
        self.PB_connect.setText(QtCore.QCoreApplication.translate(
            "AddRoomSensorWindow", "Sto cercando..."))

    # TODO:
    def on_PB_connect_released(self):
        self.PB_connect.setEnabled(False)
        roomName = self.LE_room.text()
        connection.connection()
        

    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_connect.pressed.connect(self.on_PB_connect_pressed)
        self.PB_connect.released.connect(self.on_PB_connect_released)
        self.LE_room.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)

    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def close(self):
        self.roomWindow.close()

    def setupUi(self, AddRoomSensorWindow):
        self.roomWindow = AddRoomSensorWindow
        self.roomWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        AddRoomSensorWindow.setObjectName("AddRoomSensorWindow")
        AddRoomSensorWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(10)
        AddRoomSensorWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(AddRoomSensorWindow)
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

        self.PB_ok = QtWidgets.QPushButton(self.centralwidget)
        self.PB_ok.setGeometry(QtCore.QRect(690, 350, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_ok.setFont(font)
        self.PB_ok.setObjectName("PB_ok")
        self.PB_goBack = QtWidgets.QPushButton(self.centralwidget)
        self.PB_goBack.setGeometry(QtCore.QRect(0, 350, 111, 100))
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

        self.PB_connect = QtWidgets.QPushButton(self.centralwidget)
        self.PB_connect.setGeometry(QtCore.QRect(220, 320, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_connect.setFont(font)
        self.PB_connect.setObjectName("PB_connect")
        AddRoomSensorWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AddRoomSensorWindow)
        self.statusbar.setObjectName("statusbar")
        AddRoomSensorWindow.setStatusBar(self.statusbar)

        self.activeFunctionsConnection()
        self.retranslateUi(AddRoomSensorWindow)
        QtCore.QMetaObject.connectSlotsByName(AddRoomSensorWindow)

    def retranslateUi(self, AddRoomSensorWindow):
        _translate = QtCore.QCoreApplication.translate
        AddRoomSensorWindow.setWindowTitle(
            _translate("AddRoomSensorWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(
            _translate("AddRoomSensorWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate(
            "AddRoomSensorWindow", "dd - MM - yyyy"))
        self.PB_ok.setText(_translate("AddRoomSensorWindow", "Ok"))
        self.PB_goBack.setText(_translate("AddRoomSensorWindow", "<"))
        self.LE_room.setPlaceholderText(_translate(
            "AddRoomSensorWindow", "Inserire nome della stanza"))

        self.label_RoomSettings.setText(_translate("AddRoomSensorWindow", "Room\n"
                                                   "Settings"))
        self.label_RoomName.setText(_translate(
            "AddRoomSensorWindow", "Room Name:"))

        self.PB_connect.setText(_translate(
            "AddRoomSensorWindow", "Associa sensore..."))
