# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'networkSettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import settingsWindow


class Ui_NetworkSettingsWindow(object):

    def on_PB_goBack_clicked(self):
        self.close()
        self.networkSettingsWindow = QtWidgets.QMainWindow()
        self.uiSettingsWindow = settingsWindow.Ui_SettingsWindow()
        self.uiSettingsWindow.setupUi(self.networkSettingsWindow)
        self.networkSettingsWindow.show()

    def on_PB_showPassword_pressed(self):
        self.LE_networkPassword.setEchoMode(QtWidgets.QLineEdit.Normal)

    def on_PB_showPassword_released(self):
        self.LE_networkPassword.setEchoMode(QtWidgets.QLineEdit.Password)

    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_showPassword.pressed.connect(self.on_PB_showPassword_pressed)
        self.PB_showPassword.released.connect(self.on_PB_showPassword_released)

    def close(self):
        self.networkSettingsWindow.close()

    def setupUi(self, NetworkSettingsWindow):
        self.networkSettingsWindow = NetworkSettingsWindow

        NetworkSettingsWindow.setObjectName("NetworkSettingsWindow")
        NetworkSettingsWindow.resize(800, 480)
        self.centralwidget = QtWidgets.QWidget(NetworkSettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(110, 0, 571, 61))
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
        self.LE_networkSSID = QtWidgets.QLineEdit(self.centralwidget)
        self.LE_networkSSID.setGeometry(QtCore.QRect(110, 130, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LE_networkSSID.setFont(font)
        self.LE_networkSSID.setObjectName("LE_networkSSID")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(677, 0, 121, 61))
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
        self.LE_networkPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.LE_networkPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LE_networkPassword.setGeometry(QtCore.QRect(110, 240, 581, 61))
        self.PB_showPassword = QtWidgets.QPushButton(self.centralwidget)
        self.PB_showPassword.setGeometry(QtCore.QRect(700, 240, 71, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_showPassword.setFont(font)
        self.PB_showPassword.setObjectName("PB_showPassword")
        self.LE_networkPassword.setFont(font)
        self.LE_networkPassword.setObjectName("LE_networkPassword")
        self.PB_goBack = QtWidgets.QPushButton(self.centralwidget)
        self.PB_goBack.setGeometry(QtCore.QRect(0, 350, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_goBack.setFont(font)
        self.PB_goBack.setObjectName("PB_goBack")
        self.PB_connect = QtWidgets.QPushButton(self.centralwidget)
        self.PB_connect.setGeometry(QtCore.QRect(220, 320, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_connect.setFont(font)
        self.PB_connect.setObjectName("PB_connect")
        self.label_NetworkSettings = QtWidgets.QLabel(self.centralwidget)
        self.label_NetworkSettings.setGeometry(QtCore.QRect(-10, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_NetworkSettings.setFont(font)
        self.label_NetworkSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_NetworkSettings.setObjectName("label_NetworkSettings")
        self.label_NetworkSSID = QtWidgets.QLabel(self.centralwidget)
        self.label_NetworkSSID.setGeometry(QtCore.QRect(100, 80, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_NetworkSSID.setFont(font)
        self.label_NetworkSSID.setAlignment(QtCore.Qt.AlignCenter)
        self.label_NetworkSSID.setObjectName("label_NetworkSSID")
        self.label_NetworkPassword = QtWidgets.QLabel(self.centralwidget)
        self.label_NetworkPassword.setGeometry(QtCore.QRect(100, 190, 211, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_NetworkPassword.setFont(font)
        self.label_NetworkPassword.setAlignment(QtCore.Qt.AlignCenter)
        self.label_NetworkPassword.setObjectName("label_NetworkPassword")
        NetworkSettingsWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(NetworkSettingsWindow)
        self.statusbar.setObjectName("statusbar")
        NetworkSettingsWindow.setStatusBar(self.statusbar)

        self.activeFunctionsConnection()
        self.retranslateUi(NetworkSettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(NetworkSettingsWindow)

    def retranslateUi(self, NetworkSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        NetworkSettingsWindow.setWindowTitle(
            _translate("NetworkSettingsWindow", "MainWindow"))
        self.dateEdit.setDisplayFormat(
            _translate("NetworkSettingsWindow", "dd - MM - yyyy"))
        self.LE_networkSSID.setPlaceholderText(
            _translate("NetworkSettingsWindow", "Inserire Network SSID"))
        self.timeEdit.setDisplayFormat(
            _translate("NetworkSettingsWindow", "HH : mm"))
        self.PB_ok.setText(_translate("NetworkSettingsWindow", "Ok"))
        self.LE_networkPassword.setPlaceholderText(
            _translate("NetworkSettingsWindow", "Inserire Network Password"))
        self.PB_goBack.setText(_translate("NetworkSettingsWindow", "<"))
        self.PB_connect.setText(_translate(
            "NetworkSettingsWindow", "Connetti..."))
        self.label_NetworkSettings.setText(_translate("NetworkSettingsWindow", "Network\n"
                                                      "Settings"))
        self.label_NetworkSSID.setText(
            _translate("NetworkSettingsWindow", "Network SSID:"))
        self.label_NetworkPassword.setText(
            _translate("NetworkSettingsWindow", "Network Password:"))
        self.PB_showPassword.setText(
            _translate("networkSettingsWindow", "Show"))
