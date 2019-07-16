import os
import sys
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import sensorValveProgramWindow
from Devices.connectionpy import connection_actuator_cold
import data
from database_manager import database_manager


from PyQt5 import QtCore, QtGui, QtWidgets


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


class Ui_ACSettingsWindow(object):

    db = None
    actualRoomIndex = 0
    actualRoomID = 0
    actualRoomName = ""

    roomDataConfiguration = None
    actuatorsConfiguration = None
    
    def initDB(self, db):
        self.db = db

     def searchActualRoomID(self):
        self.configuration = database_manager.get_configuration(self.db)

        self.actualRoomID = self.configuration["rooms_settings"][self.actualRoomIndex]["room"]

    def reloadRoomData(self):
        self.actuatorsConfiguration = database_manager.get_actuators_configuration(self.db)
        self.roomDataConfiguration = database_manager.get_roomData_configuration(self.db)

    def on_PB_goBack_clicked(self):
        self.close()
        self.acSettingsWindow = QtWidgets.QMainWindow()
        self.uiSensorValveProgramWindow = sensorValveProgramWindow.Ui_SensorValveProgramWindow()
        self.uiSensorValveProgramWindow.setupUi(self.acSettingsWindow, self.db, self.actualRoomIndex, self.actualRoomName)
        self.acSettingsWindow.showMaximized()

    def on_PB_connectAc_pressed(self):
        self.PB_connectAc.setText(QtCore.QCoreApplication.translate(
            "ACSettingsWindow", "Connecting..."))

    def on_PB_connectAc_released(self):
        acID = self.LE_ac.text()

        # Check se il campo inserito è vuoto
        if (acID == "" or not(str(acID).isdecimal())):
            print("AirConditioner ID empty or non numerical!")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Insert a valid numerical-only ID")
            msg.setWindowTitle("Error")
            msg.exec_()
            self.PB_connectAc.setEnabled(True)
            self.PB_connectAc.setText(QtCore.QCoreApplication.translate(
                            "ACSettingsWindow", "Connect"))
        else:
            # Check se ID attuatore già presente
            # Devo però controllare anche che l'actuator sia di tipo freddo COLD = condizionatore
            flag = 0
            actualNumAc = len(self.actuatorsConfiguration["conf"])
            for i in range(0, actualNumAc):
                if (str(acID).lower() == str(self.actuatorsConfiguration["conf"][i]["actuatorID"]).lower() and self.actuatorsConfiguration["conf"][i]["type"] == "cold"):
                    flag = 1
                    break
            if (flag == 1): # L'ID AC esiste già, ritorna errore
                print("ID AirConditioner already IN!")
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText(
                    "This AirConditioner has been already connected!")
                msg.setWindowTitle("Error")
                msg.exec_()
                self.PB_connectAc.setText(QtCore.QCoreApplication.translate(
                            "ACSettingsWindow", "Connect"))
                return

            net_SSID = data.networkData["net_SSID"]
            net_PWD = data.networkData["net_PWD"]
            # net_SSID = "ciao"
            # net_PWD = "bela"

            if (net_SSID == "" or net_PWD == ""):
                print("Net SSID and NET PWD cannot be empty! Maybe Raspone is not connected to network...")

                print("No SSID and PWD found when connecting AC")
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText(
                    "Please connect the thermostat to WiFi before adding and AC")
                msg.setWindowTitle("Error")
                msg.exec_()

            else: 
                returnID = connection_actuator_cold.connection(acID, actualRoomID, net_SSID, net_PWD)    
                # returnID = 0
                if (returnID == 0):
                    print("OK! AC is being connected!")

                    if (len(self.actuatorsConfiguration["conf"]) == 1 and str(self.actuatorsConfiguration["conf"][0]["actuatorID"]) == ""):
                        self.actuatorsConfiguration["conf"][0]["actuatorID"] = acID
                        self.actuatorsConfiguration["conf"][0]["type"] = "cold"

                    else:
                        self.actuatorsConfiguration["conf"].append({"actuatorID" : acID, "type": "cold", "valves" : [{"valveID": ""}]})

                    if (len(self.roomDataConfiguration["conf"][self.actualRoomIndex]["actuators"]) == 1 and str(self.roomDataConfiguration["conf"][self.actualRoomIndex]["actuators"][0]["actuatorID"]) == ""):
                        self.roomDataConfiguration["conf"][self.actualRoomIndex]["actuators"][0]["actuatorID"] = acID
                        self.roomDataConfiguration["conf"][self.actualRoomIndex]["actuators"][0]["type"] = "cold"
                    else:
                        self.roomDataConfiguration["conf"][self.actualRoomIndex]["actuators"].append({"actuatorID": acID, "type": "cold", "valves": [{"valveID": ""}]})

                    print("\t --> COMMIT actuatorsConfiguration")    
                    database_manager.update_actuators_configuration(self.db, self.actuatorsConfiguration)
                    print("\t --> COMMIT roomDataConfiguration")
                    database_manager.update_roomData_configuration(self.db, self.roomDataConfiguration)

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setInformativeText(
                        "AC connected!")
                    msg.setWindowTitle("Connected!")
                    msg.exec_()

                    self.PB_connectAc.setText(QtCore.QCoreApplication.translate(
                            "ACSettingsWindow", "Connect"))

                elif (returnID == -1):
                    print("AC not found in BT proximity, check AC ID pliz")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "AC ID not found, please retry")
                    msg.setWindowTitle("Errore")
                    msg.exec_()
                    
                    self.PB_connectAc.setText(QtCore.QCoreApplication.translate(
                            "ACSettingsWindow", "Not connected, please retry..."))
                    self.PB_connectAc.setEnabled(True)

                elif (returnID == -2):
                    print("Cannot connect, Bluetooth Socket error.")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "AC not connected, error in BT socket")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectAc.setText(QtCore.QCoreApplication.translate(
                            "ACSettingsWindow", "Not connected, please retry..."))
                    self.PB_connectAc.setEnabled(True)

                elif (returnID == -3):
                    print("Nothing received from AC, did you pushed the button?")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Push the AC button BEFORE the connection attempt!")
                    msg.setWindowTitle("Error")
                    msg.exec_()

                    self.PB_connectAc.setText(QtCore.QCoreApplication.translate(
                            "ACSettingsWindow", "Not connected, please retry..."))
                    self.PB_connectAc.setEnabled(True)

                elif (returnID == -4):
                    print("Cannot connect, no transmission from actACuator")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "No transmission from the AC")
                    msg.setWindowTitle("Error")
                    msg.exec_()

                    self.PB_connectAc.setText(QtCore.QCoreApplication.translate(
                            "ACSettingsWindow", "Not connected, please retry..."))
                    self.PB_connectAc.setEnabled(True)

                elif (returnID == -5):
                    print("Cannot connect, error transmitting SSID")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Error while transferring the SSID to the AC")
                    msg.setWindowTitle("Error")
                    msg.exec_()

                    self.PB_connectAc.setText(QtCore.QCoreApplication.translate(
                            "ACSettingsWindow", "Not connected, please retry..."))
                    self.PB_connectAc.setEnabled(True)

                elif (returnID == -6):
                    print("Cannot connect, error transmitting WIFI Password")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Error while tansferring the network password to the AC")
                    msg.setWindowTitle("Error")
                    msg.exec_()

                    self.PB_connectAc.setText(QtCore.QCoreApplication.translate(
                            "ACSettingsWindow", "Not connected, please retry..."))
                    self.PB_connectAc.setEnabled(True)

    def on_PB_deleteAc_clicked(self):
        acID = self.LE_ac.text()

        if (acID == "" or not(str(acID).isdecimal())):
            print("AirConditioner ID empty or non numerical!")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Insert a valid numerical-only ID")
            msg.setWindowTitle("Error")
            msg.exec_()

        else: # ID AC inserito correttamente
            # Cerca l'AC, se esiste eliminalo
            flag = 0
            actualNumActuators = len(self.actuatorsConfiguration["conf"])
            for i in range(0, actualNumActuators):
                if (str(acID).lower() == str(self.actuatorsConfiguration["conf"][i]["actuatorID"]).lower() and str(self.actuatorsConfiguration["conf"][i]["type"]) == "cold"):
                    del self.actuatorsConfiguration["conf"][i]
                    flag = 1
                    break
                    
            if (flag == 1): 

                flag = 0
                actualNumActuators = len(self.roomDataConfiguration["conf"][self.actualRoomIndex]["actuators"])
                for i in range(0, actualNumActuators):
                    if (str(acID).lower() == str(self.roomDataConfiguration["conf"][self.actualRoomIndex]["actuators"][i]["actuatorID"]).lower() and str(self.roomDataConfiguration["conf"][self.actualRoomIndex]["actuators"][i]["type"]) == "cold"):
                        del self.roomDataConfiguration["conf"][self.actualRoomIndex]["actuators"][i]
                        flag = 1
                        break

                print("\t --> COMMIT")
                database_manager.update_actuators_configuration(self.db, self.actuatorsConfiguration)
                database_manager.update_roomData_configuration(self.db, self.roomDataConfiguration)

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
                
        self.PB_deleteAc.setText(QtCore.QCoreApplication.translate(
            "DeleteActuatorWindow", "Delete"))
        pass

    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_connectAc.pressed.connect(self.on_PB_connectAc_pressed)
        self.PB_connectAc.released.connect(self.on_PB_connectAc_released)
        self.PB_deleteAc.clicked.connect(self.on_PB_deleteAc_clicked)

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
        self.acSettingsWindow.close()

    def setupUi(self, ACSettingsWindow, db, actualRoomIndex, actualRoomName):
        self.acSettingsWindow = ACSettingsWindow
        self.acSettingsWindow.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)

        ACSettingsWindow.setObjectName("ACSettingsWindow")
        ACSettingsWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(10)
        ACSettingsWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(ACSettingsWindow)
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
        self.label_SensorSettings = QtWidgets.QLabel(self.centralwidget)
        self.label_SensorSettings.setGeometry(QtCore.QRect(-10, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_SensorSettings.setFont(font)
        self.label_SensorSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_SensorSettings.setObjectName("label_SensorSettings")
        self.label_AcID = QtWidgets.QLabel(self.centralwidget)
        self.label_AcID.setGeometry(QtCore.QRect(150, 150, 241, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_AcID.setFont(font)
        self.label_AcID.setAlignment(QtCore.Qt.AlignCenter)
        self.label_AcID.setObjectName("label_AcID")
        self.PB_connectAc = QtWidgets.QPushButton(self.centralwidget)
        self.PB_connectAc.setGeometry(QtCore.QRect(170, 310, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_connectAc.setFont(font)
        self.PB_connectAc.setObjectName("PB_connectAc")
        self.label_RoomName = QtWidgets.QLabel(self.centralwidget)
        self.label_RoomName.setGeometry(QtCore.QRect(210, 90, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_RoomName.setFont(font)
        self.label_RoomName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_RoomName.setObjectName("label_RoomName")
        self.PB_deleteAc = QtWidgets.QPushButton(self.centralwidget)
        self.PB_deleteAc.setGeometry(QtCore.QRect(470, 310, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_deleteAc.setFont(font)
        self.PB_deleteAc.setObjectName("PB_deleteAc")
        self.LE_ac = MyQLineEdit(self.centralwidget)
        self.LE_ac.setGeometry(QtCore.QRect(170, 200, 531, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LE_ac.setFont(font)
        self.LE_ac.setObjectName("LE_ac")
        ACSettingsWindow.setCentralWidget(self.centralwidget)


        self.initDB(db)
        self.reloadRoomData()
        self.actualRoomIndex = actualRoomIndex
        self.actualRoomName = actualRoomName
        self.searchActualRoomID()

        self.timer = QTimer()

        self.activeFunctionsConnection()
        self.reloadRoomData()

        self.retranslateUi(ACSettingsWindow)

    def retranslateUi(self, ACSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        ACSettingsWindow.setWindowTitle(_translate("ACSettingsWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(_translate("ACSettingsWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate("ACSettingsWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("ACSettingsWindow", "<"))
        self.label_SensorSettings.setText(_translate("ACSettingsWindow", "A/C\n"
"Settings"))
        self.label_AcID.setText(_translate("ACSettingsWindow", "AirConditioner ID:"))
        self.PB_connectAc.setText(_translate("ACSettingsWindow", "Connect"))
        self.label_RoomName.setText(_translate("ACSettingsWindow", "Actual Room: " + str(self.actualRoomName)))
        self.PB_deleteAc.setText(_translate("ACSettingsWindow", "Delete"))
        self.LE_ac.setPlaceholderText(_translate("ACSettingsWindow", "Insert ID of the AirConditioner"))