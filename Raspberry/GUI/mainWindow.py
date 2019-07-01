# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
import settingsWindow
import addRoomSensorWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import sys
import os


# from addRoomSensorWindow import Ui_AddRoomSensorWindow
# Time and DateTime section


class Ui_MainWindow(object):

    def on_PB_roomList_clicked(self):
        self.close()
        self.mainWindow = QtWidgets.QMainWindow()
        self.uiRoomSensorWindow = addRoomSensorWindow.Ui_AddRoomSensorWindow()
        self.uiRoomSensorWindow.setupUi(self.mainWindow)
        self.mainWindow.showMaximized()

    def on_PB_settings_clicked(self):
        self.close()
        self.mainWindow = QtWidgets.QMainWindow()
        self.uiSettingsWindow = settingsWindow.Ui_SettingsWindow()
        self.uiSettingsWindow.setupUi(self.mainWindow)
        self.mainWindow.showMaximized()

    def activeFunctionsConnection(self):
        # PB_roomList
        self.PB_roomList.clicked.connect(self.on_PB_roomList_clicked)
        self.PB_settings.clicked.connect(self.on_PB_settings_clicked)
        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)

    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def close(self):
        self.mainWindow.close()

    def setupUi(self, MainWindow):

        self.mainWindow = MainWindow
        self.mainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.PB_tempIncrease = QtWidgets.QPushButton(self.centralwidget)
        self.PB_tempIncrease.setGeometry(QtCore.QRect(689, 120, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_tempIncrease.setFont(font)
        self.PB_tempIncrease.setObjectName("PB_tempIncrease")
        self.PB_tempDecrease = QtWidgets.QPushButton(self.centralwidget)
        self.PB_tempDecrease.setGeometry(QtCore.QRect(690, 250, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_tempDecrease.setFont(font)
        self.PB_tempDecrease.setObjectName("PB_tempDecrease")

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)

        # Date and Time widgets
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(120, 0, 571, 61))
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
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(260, 140, 281, 181))
        self.lcdNumber.setObjectName("lcdNumber")
        self.PB_settings = QtWidgets.QPushButton(self.centralwidget)
        self.PB_settings.setGeometry(QtCore.QRect(0, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_settings.setFont(font)
        self.PB_settings.setObjectName("PB_settings")
        self.PB_program = QtWidgets.QPushButton(self.centralwidget)
        self.PB_program.setGeometry(QtCore.QRect(260, 340, 71, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_program.setFont(font)
        self.PB_program.setObjectName("PB_program")
        self.PB_manual = QtWidgets.QPushButton(self.centralwidget)
        self.PB_manual.setGeometry(QtCore.QRect(330, 340, 71, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_manual.setFont(font)
        self.PB_manual.setObjectName("PB_manual")
        self.PB_winterSummer = QtWidgets.QPushButton(self.centralwidget)
        self.PB_winterSummer.setGeometry(QtCore.QRect(470, 340, 71, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_winterSummer.setFont(font)
        self.PB_winterSummer.setObjectName("PB_winterSummer")
        self.PB_onOff = QtWidgets.QPushButton(self.centralwidget)
        self.PB_onOff.setGeometry(QtCore.QRect(400, 340, 71, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_onOff.setFont(font)
        self.PB_onOff.setObjectName("PB_onOff")
        self.PB_roomList = QtWidgets.QPushButton(self.centralwidget)
        self.PB_roomList.setGeometry(QtCore.QRect(50, 420, 701, 34))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_roomList.setFont(font)
        self.PB_roomList.setObjectName("PB_roomList")
        self.PB_prevRoom = QtWidgets.QPushButton(self.centralwidget)
        self.PB_prevRoom.setGeometry(QtCore.QRect(0, 420, 51, 34))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_prevRoom.setFont(font)
        self.PB_prevRoom.setObjectName("PB_prevRoom")
        self.PB_nextRoom = QtWidgets.QPushButton(self.centralwidget)
        self.PB_nextRoom.setGeometry(QtCore.QRect(750, 420, 51, 34))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_nextRoom.setFont(font)
        self.PB_nextRoom.setObjectName("PB_nextRoom")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.activeFunctionsConnection()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PB_tempIncrease.setText(_translate("MainWindow", "+"))
        self.PB_tempDecrease.setText(_translate("MainWindow", "-"))
        self.dateEdit.setDisplayFormat(
            _translate("MainWindow", "dd - MM - yyyy"))
        self.timeEdit.setDisplayFormat(_translate("MainWindow", "HH : mm"))
        self.PB_settings.setText(_translate("MainWindow", "Settings"))
        self.PB_program.setText(_translate("MainWindow", "P"))
        self.PB_manual.setText(_translate("MainWindow", "M"))
        self.PB_winterSummer.setText(_translate("MainWindow", "Inv/Est"))
        self.PB_onOff.setText(_translate("MainWindow", "On/Off"))
        self.PB_roomList.setText(_translate("MainWindow", "PushButton"))
        self.PB_prevRoom.setText(_translate("MainWindow", "<"))
        self.PB_nextRoom.setText(_translate("MainWindow", ">"))
