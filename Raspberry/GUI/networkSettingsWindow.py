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
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer


os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

import networkConnection
import settingsWindow
import subprocess
import data


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


class Ui_NetworkSettingsWindow(object):

    db = None

    def initDB(self, db):
        self.db = db

    def on_PB_goBack_clicked(self):
        self.close()
        self.networkSettingsWindow = QtWidgets.QMainWindow()
        self.uiSettingsWindow = settingsWindow.Ui_SettingsWindow()
        self.uiSettingsWindow.setupUi(self.networkSettingsWindow, self.db)
        self.networkSettingsWindow.showMaximized()

    def on_PB_showPassword_pressed(self):
        self.LE_networkPassword.setEchoMode(QtWidgets.QLineEdit.Normal)

    def on_PB_showPassword_released(self):
        self.LE_networkPassword.setEchoMode(QtWidgets.QLineEdit.Password)

    def on_PB_connect_pressed(self):
        self.PB_connect.setText(QtCore.QCoreApplication.translate(
            "NetworkSettingsWindow", "Connecting, please wait..."))

    def on_PB_connect_released(self):
        self.PB_connect.setEnabled(False)
        networkConnection.net_SSID = self.LE_networkSSID.text()
        networkConnection.net_PWD = self.LE_networkPassword.text()

        if len(networkConnection.net_PWD) < 8 or len(networkConnection.net_PWD) > 63:
            if len(networkConnection.net_PWD) != 0:
                print("ERROR!! Password must be >= 8 characters and <= 63 characters")
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText(
                    "Password must be at least 8 characters and at most 63 characters")
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            subprocess.Popen(["killall", "onboard"])
            returnID = networkConnection.connectToNetwork()
            if (returnID == 0):
                print("Connected to network")
                self.PB_connect.setText(QtCore.QCoreApplication.translate(
                    "NetworkSettingsWindow", "Connected!"))
                self.PB_connect.setEnabled(False)

                print("Tutto OK, salvo le credenziali nel file...")
                self.saveNetCredentials(networkConnection.net_SSID, networkConnection.net_PWD)

            elif (returnID == 1):
                print("Not connected, no feedback received from iwgetid")
                self.PB_connect.setText(QtCore.QCoreApplication.translate(
                    "NetworkSettingsWindow", "Not connected, retry"))
                self.PB_connect.setEnabled(True)

            elif (returnID == -1):
                print("Not connected, SSID not found")
                self.PB_connect.setText(QtCore.QCoreApplication.translate(
                    "NetworkSettingsWindow", "Not connected, retry"))
                self.PB_connect.setEnabled(True)

    def checkNetworkConnection(self):
        returnID = networkConnection.checkNetworkConnection()
        if (returnID == 0):
            networkConnection.isConnected = True
        else:
            networkConnection.isConnected = False

    def on_LE_networkSSID_clicked(self):
        if (self.LE_networkSSID.isModified() or self.LE_networkPassword.isModified()):
            self.PB_connect.setText(QtCore.QCoreApplication.translate(
                "NetworkSettingsWindow", "Connect..."))
            self.PB_connect.setEnabled(True)

    def on_LE_networkPassword_clicked(self):
        if (self.LE_networkSSID.isModified() or self.LE_networkPassword.isModified()):
            self.PB_connect.setText(QtCore.QCoreApplication.translate(
                "NetworkSettingsWindow", "Connect..."))
            self.PB_connect.setEnabled(True)

    def __handleTextChanged(self, text):
        if not self.LE_networkSSID.hasFocus:
            self.LE_networkSSID._beforeSSID = text
        if not self.LE_networkPassword.hasFocus:
            self.LE_networkPassword._beforePWD = text

    def __handleEditingFinished(self):
        beforeSSID, afterSSID = self.LE_networkSSID._beforeSSID, self.LE_networkSSID.text()
        if beforeSSID != afterSSID:
            self.LE_networkSSID._beforeSSID = afterSSID
            self.LE_networkSSID.textChanged.emit(afterSSID)
            self.PB_connect.setText(QtCore.QCoreApplication.translate(
                "NetworkSettingsWindow", "Connect..."))
            self.PB_connect.setEnabled(True)
        beforePWD, afterPWD = self.LE_networkPassword._beforePWD, self.LE_networkPassword.text()
        if beforePWD != afterPWD:
            self.LE_networkPassword._beforePWD = afterPWD
            self.LE_networkPassword.textChanged.emit(afterPWD)
            self.PB_connect.setText(QtCore.QCoreApplication.translate(
                "NetworkSettingsWindow", "Connect..."))
            self.PB_connect.setEnabled(True)

    def saveNetCredentials(self, net_SSID, net_PWD):
        data.networkData["net_SSID"] = net_SSID
        data.networkData["net_PWD"] = net_PWD

        print("net_SSID salvato: " + str(data.networkData["net_SSID"]))
        print("net_PWD salvato: " + str(data.networkData["net_PWD"]))
        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, './../netCredentials.json')

        print("Salvo i dati nel file JSON")
        try:
            with open(filename, 'w') as json_file:
                json.dump(data.networkData, json_file)
        except:
            pass

    def activeFunctionsConnection(self):
        networkConnection.isConnected = False

        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_showPassword.pressed.connect(self.on_PB_showPassword_pressed)
        self.PB_showPassword.released.connect(self.on_PB_showPassword_released)
        self.PB_connect.pressed.connect(self.on_PB_connect_pressed)
        self.PB_connect.released.connect(self.on_PB_connect_released)

        self.LE_networkSSID.editingFinished.connect(
            self.__handleEditingFinished)
        self.LE_networkSSID.textChanged.connect(self.__handleTextChanged)
        self.LE_networkSSID._beforeSSID = ""

        self.LE_networkPassword.editingFinished.connect(
            self.__handleEditingFinished)
        self.LE_networkPassword.textChanged.connect(self.__handleTextChanged)
        self.LE_networkPassword._beforePWD = ""

        self.LE_networkSSID.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.LE_networkPassword.setFocusPolicy(QtCore.Qt.StrongFocus)

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
        self.networkSettingsWindow.close()

    def setupUi(self, NetworkSettingsWindow, db):
        self.networkSettingsWindow = NetworkSettingsWindow
        self.networkSettingsWindow.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)

        NetworkSettingsWindow.setObjectName("NetworkSettingsWindow")
        NetworkSettingsWindow.resize(800, 480)
        self.centralwidget = QtWidgets.QWidget(NetworkSettingsWindow)
        self.centralwidget.setObjectName("centralwidget")

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)

        self.LE_networkSSID = MyQLineEdit(self.centralwidget)
        self.LE_networkSSID.setGeometry(QtCore.QRect(110, 130, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LE_networkSSID.setFont(font)
        self.LE_networkSSID.setObjectName("LE_networkSSID")

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

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LE_networkPassword = MyQLineEdit(self.centralwidget)
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
        self.PB_goBack.setGeometry(QtCore.QRect(0, 380, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_goBack.setFont(font)
        self.PB_goBack.setObjectName("PB_goBack")
        self.PB_connect = QtWidgets.QPushButton(self.centralwidget)
        self.PB_connect.setGeometry(QtCore.QRect(220, 320, 361, 61))
        self.PB_connect.setEnabled(False)
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

        self.initDB(db)

        self.activeFunctionsConnection()

        self.checkNetworkConnection()

        self.retranslateUi(NetworkSettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(NetworkSettingsWindow)

    def retranslateUi(self, NetworkSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        NetworkSettingsWindow.setWindowTitle(
            _translate("NetworkSettingsWindow", "MainWindow"))
        self.dateEdit.setDisplayFormat(
            _translate("NetworkSettingsWindow", "dd - MM - yyyy"))
        self.LE_networkSSID.setPlaceholderText(
            _translate("NetworkSettingsWindow", "Insert Network name"))
        self.timeEdit.setDisplayFormat(
            _translate("NetworkSettingsWindow", "HH : mm"))
        self.LE_networkPassword.setPlaceholderText(
            _translate("NetworkSettingsWindow", "Insert Network password"))
        self.PB_goBack.setText(_translate("NetworkSettingsWindow", "<"))

        # Controlla se il sistema è già connesso a una rete oppure no
        if (networkConnection.isConnected == True):
            # Se è connesso disabilita il tasto per connettere, per riabilitarlo
            # sarà necessario inserire del testo nei lineEdit
            self.PB_connect.setText(_translate(
                "NetworkSettingsWindow", "Connected!"))
            self.PB_connect.setEnabled(False)
            self.LE_networkSSID.setPlaceholderText(
                _translate("NetworkSettingsWindow",
                           "Connected!"))
        else:
            self.PB_connect.setText(_translate(
                "NetworkSettingsWindow", "Connect..."))
            self.PB_connect.setEnabled(False)

        self.label_NetworkSettings.setText(_translate("NetworkSettingsWindow", "Network\n"
                                                      "Settings"))
        self.label_NetworkSSID.setText(
            _translate("NetworkSettingsWindow", "Network SSID:"))
        self.label_NetworkPassword.setText(
            _translate("NetworkSettingsWindow", "Network Password:"))
        self.PB_showPassword.setText(
            _translate("networkSettingsWindow", "Show"))
