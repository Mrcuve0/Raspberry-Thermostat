# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sensorValveProgramWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

# TODO: Add window imports here
import mainWindow


class Ui_SensorValveProgramWindow(object):

    # TODO: aggiungi apertura della finestra dove puoi aggiungere un sensore alla stanza
    def on_PB_sensor_clicked(self):
        pass
    
    # TODO: aggiungi apertura della finestra dove puoi aggiungere un relè all'attuatore che preferisci
    def on_PB_valve_clicked(self):
        pass

    # TODO: aggiungi apertura della finestra dove puoi aggiungere il cronoprogramma relativo a questa finestra
    def on_PB_program_clicked(self):
        pass

    def on_PB_goBack_clicked(self):
        self.close()
        self.sensorValveProgramWindow = QtWidgets.QMainWindow()
        self.uiMainWindow = mainWindow.Ui_MainWindow()
        self.uiMainWindow.setupUi(self.sensorValveProgramWindow)
        self.sensorValveProgramWindow.showMaximized()

    def activeFunctionsConnection(self):
        self.PB_sensor.clicked.connect(self.on_PB_sensor_clicked)
        self.PB_valve.clicked.connect(self.on_PB_valve_clicked)
        self.PB_timeProgram.clicked.connect(self.on_PB_program_clicked)
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)

    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def close(self):
        self.sensorValveProgramWindow.close()

    def setupUi(self, SensorValveProgramWindow):

        self.sensorValveProgramWindow = SensorValveProgramWindow
        self.sensorValveProgramWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        SensorValveProgramWindow.setObjectName("SensorValveProgramWindow")
        SensorValveProgramWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        SensorValveProgramWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(SensorValveProgramWindow)
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
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

        self.PB_goBack = QtWidgets.QPushButton(self.centralwidget)
        self.PB_goBack.setGeometry(QtCore.QRect(0, 350, 111, 100))
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
        self.PB_sensor.setGeometry(QtCore.QRect(20, 160, 181, 121))
        self.PB_sensor.setObjectName("PB_sensor")
        self.PB_valve = QtWidgets.QPushButton(self.centralwidget)
        self.PB_valve.setGeometry(QtCore.QRect(320, 160, 181, 121))
        self.PB_valve.setObjectName("PB_valve")
        self.PB_timeProgram = QtWidgets.QPushButton(self.centralwidget)
        self.PB_timeProgram.setGeometry(QtCore.QRect(600, 160, 181, 121))
        self.PB_timeProgram.setObjectName("PB_timeProgram")
        SensorValveProgramWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SensorValveProgramWindow)
        self.statusbar.setObjectName("statusbar")
        SensorValveProgramWindow.setStatusBar(self.statusbar)

        self.activeFunctionsConnection()
        self.retranslateUi(SensorValveProgramWindow)
        QtCore.QMetaObject.connectSlotsByName(SensorValveProgramWindow)

    def retranslateUi(self, SensorValveProgramWindow):

        _translate = QtCore.QCoreApplication.translate
        SensorValveProgramWindow.setWindowTitle(_translate("SensorValveProgramWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(_translate("SensorValveProgramWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate("SensorValveProgramWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("SensorValveProgramWindow", "<"))
        self.label_RoomSettings.setText(_translate("SensorValveProgramWindow", "Room\n"
"Settings"))
        self.label_RoomName.setText(_translate("SensorValveProgramWindow", "<Room Name Here>"))
        self.PB_sensor.setText(_translate("SensorValveProgramWindow", "Imposta / Vedi\n"
"Sensore"))
        self.PB_valve.setText(_translate("SensorValveProgramWindow", "Imposta / Vedi\n"
"Valvole"))
        self.PB_timeProgram.setText(_translate("SensorValveProgramWindow", "Imposta / Vedi\n"
"CronoProgramma"))
