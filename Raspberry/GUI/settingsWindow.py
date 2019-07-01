# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import mainWindow
import networkSettingsWindow


class Ui_SettingsWindow(object):

    def on_PB_goBack_clicked(self):
        self.close()
        self.settingsWindow = QtWidgets.QMainWindow()
        self.uiMainWindow = mainWindow.Ui_MainWindow()
        self.uiMainWindow.setupUi(self.settingsWindow)
        self.settingsWindow.showMaximized()

    def on_PB_network_clicked(self):
        self.close()
        self.settingsWindow = QtWidgets.QMainWindow()
        self.uiNetworkSettingsWindow = networkSettingsWindow.Ui_NetworkSettingsWindow()
        self.uiNetworkSettingsWindow.setupUi(self.settingsWindow)
        self.settingsWindow.showMaximized()

    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_network.clicked.connect(self.on_PB_network_clicked)
        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)

    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def close(self):
        self.settingsWindow.close()

    def setupUi(self, SettingsWindow):

        self.settingsWindow = SettingsWindow
        self.settingsWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(800, 480)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
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

        self.PB_goBack = QtWidgets.QPushButton(self.centralwidget)
        self.PB_goBack.setGeometry(QtCore.QRect(0, 350, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_goBack.setFont(font)
        self.PB_goBack.setObjectName("PB_goBack")
        self.PB_ok = QtWidgets.QPushButton(self.centralwidget)
        self.PB_ok.setGeometry(QtCore.QRect(690, 350, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_ok.setFont(font)
        self.PB_ok.setObjectName("PB_ok")
        self.PB_network = QtWidgets.QPushButton(self.centralwidget)
        self.PB_network.setGeometry(QtCore.QRect(110, 110, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_network.setFont(font)
        self.PB_network.setObjectName("PB_network")
        self.PB_altro = QtWidgets.QPushButton(self.centralwidget)
        self.PB_altro.setGeometry(QtCore.QRect(110, 190, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_altro.setFont(font)
        self.PB_altro.setObjectName("PB_altro")
        SettingsWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SettingsWindow)
        self.statusbar.setObjectName("statusbar")
        SettingsWindow.setStatusBar(self.statusbar)

        self.activeFunctionsConnection()
        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(
            _translate("SettingsWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(_translate("SettingsWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(
            _translate("SettingsWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("SettingsWindow", "<"))
        self.PB_ok.setText(_translate("SettingsWindow", "Ok"))
        self.PB_network.setText(_translate("SettingsWindow", "Network"))
        self.PB_altro.setText(_translate("SettingsWindow", "Altro"))
