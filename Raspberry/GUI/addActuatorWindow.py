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
            subprocess.Popen(["onboard"])
        except FileNotFoundError:
            pass
        super(MyQLineEdit, self).focusInEvent(e)

    def focusOutEvent(self, e):
        subprocess.Popen(["killall", "onboard"])
        super(MyQLineEdit, self).focusOutEvent(e)


class Ui_addActuatorWindow(object):

    db = None
    actuatorsConfiguration = None

    def initDB(self, db):
        self.db = db

    def on_PB_goBack_clicked(self):
        self.close()
        self.addActuatorWindow = QtWidgets.QMainWindow()
        self.uiSettingsWindow = settingsWindow.Ui_SettingsWindow()
        self.uiSettingsWindow.setupUi(self.addActuatorWindow, self.db)
        self.addActuatorWindow.showMaximized()

    def on_PB_addActuator_pressed(self):
        self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
            "AddActuatorWindow", "Connecting, please wait..."))

    def on_PB_addActuator_released(self):
        actuatorID = self.LE_actuator.text()

        if (actuatorID == "" or not(str(actuatorID).isdecimal())):
            print("Actuator ID empty or non numerical!")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Insert a valid numerical-only ID")
            msg.setWindowTitle("Error")
            msg.exec_()
            self.PB_addActuator.setEnabled(True)
            self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Add Actuator..."))

        else: # ID attuatore inserito

            # Check se ID attuatore già presente
            flag = 0
            actualNumActuators = len(self.actuatorsConfiguration["conf"])
            for i in range(0, actualNumActuators):
                if (str(actuatorID).lower() == str(self.actuatorsConfiguration["conf"][i]["actuatorID"]).lower()):
                    flag = 1
                    break
            if (flag == 1): # L'ID Attuatore esiste già, ritorna errore
                print("ID Actuator already IN!")
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText(
                    "This actuator has been already connected!")
                msg.setWindowTitle("Error")
                msg.exec_()
                self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Connect"))
                return

            net_SSID = data.networkData["net_SSID"]
            net_PWD = data.networkData["net_PWD"]

            if (net_SSID == "" or net_PWD == ""):
                print("Net SSID and NET PWD cannot be empty! Maybe Raspone is not connected to network...")

                print("No SSID and PWD found when connecting actuator")
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText(
                    "Please connect the thermostat to WiFi before adding an actuator!")
                msg.setWindowTitle("Error")
                msg.exec_()

            else: 
                # TODO: Uncomment
                returnID = connection_actuator.connection(actuatorID, net_SSID, net_PWD)    
                # returnID = 0
                if (returnID == 0):
                    print("OK! Actuator is being connected!")

                    if (len(self.actuatorsConfiguration["conf"]) == 1 and str(self.actuatorsConfiguration["conf"][0]["actuatorID"]) == ""):
                        self.actuatorsConfiguration["conf"][0]["actuatorID"] = actuatorID
                    else:
                        self.actuatorsConfiguration["conf"].append({"actuatorID" : actuatorID, "valves" : [{"valveID": ""}]})
                    database_manager.update_actuators_configuration(self.db, self.actuatorsConfiguration)

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setInformativeText(
                        "Actuator connected!")
                    msg.setWindowTitle("Connected!")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Connect"))

                elif (returnID == -1):
                    print("Actuator not found in BT proximity, check actuator ID pliz")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Actuator ID not found, please retry")
                    msg.setWindowTitle("Errore")
                    msg.exec_()
                    
                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Not connected, please retry..."))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -2):
                    print("Cannot connect, Bluetooth Socket error.")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Actuator not connected, error in BT socket")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Not connected, please retry..."))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -3):
                    print("Nothing received from actuator, did you pushed the button?")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Push the actuator button BEFORE the connection attempt!")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Not connected, please retry..."))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -4):
                    print("Cannot connect, no transmission from actuator")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "No transmission from the actuator")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Not connected, please retry..."))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -5):
                    print("Cannot connect, error transmitting SSID")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Error while transferring the SSID to the actuator")
                    msg.setWindowTitle("Error")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Not connected, please retry..."))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -6):
                    print("Cannot connect, error transmitting WIFI Password")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Error while tansferring the network password to the actuator")
                    msg.setWindowTitle("Error")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Not connected, please retry..."))
                    self.PB_addActuator.setEnabled(True)

                # elif (returnID == -7):
                #     print("Cannot connect, error transmitting MQTT Info")

                #     msg = QtWidgets.QMessageBox()
                #     msg.setIcon(QtWidgets.QMessageBox.Critical)
                #     msg.setInformativeText(
                #         "Error while transferring MQTT info to the actuator")
                #     msg.setWindowTitle("Error")
                #     msg.exec_()

                #     self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                #             "AddActuatorWindow", "Not connected, please retry..."))
                #     self.PB_addActuator.setEnabled(True)

    def reloadRoomData(self):
        self.actuatorsConfiguration = database_manager.get_actuators_configuration(self.db)
   
    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_addActuator.pressed.connect(self.on_PB_addActuator_pressed)
        self.PB_addActuator.released.connect(self.on_PB_addActuator_released)
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

    def setupUi(self, addActuatorWindow, db):
        self.actuatorWindow = addActuatorWindow
        self.actuatorWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        addActuatorWindow.setObjectName("AddActuatorWindow")
        addActuatorWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(10)
        addActuatorWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(addActuatorWindow)
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

        self.PB_addActuator = QtWidgets.QPushButton(self.centralwidget)
        self.PB_addActuator.setGeometry(QtCore.QRect(220, 240, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_addActuator.setFont(font)
        self.PB_addActuator.setObjectName("PB_addActuator")
        addActuatorWindow.setCentralWidget(self.centralwidget)

        self.initDB(db)

        self.activeFunctionsConnection()
        self.retranslateUi(addActuatorWindow)
        QtCore.QMetaObject.connectSlotsByName(addActuatorWindow)

    def retranslateUi(self, addActuatorWindow):
        _translate = QtCore.QCoreApplication.translate
        addActuatorWindow.setWindowTitle(
            _translate("AddActuatorWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(
            _translate("AddActuatorWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate(
            "AddActuatorWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("AddActuatorWindow", "<"))
        self.LE_actuator.setPlaceholderText(_translate(
            "AddActuatorWindow", "Insert actuator ID"))

        self.label_ActuatorSettings.setText(_translate("AddActuatorWindow", "Actuator\n"
                                                   "Settings"))
        self.label_ActuatorName.setText(_translate(
            "AddActuatorWindow", "Actuator Name:"))

        self.PB_addActuator.setText(_translate(
            "AddActuatorWindow", "Add Actuator..."))
