import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import sensorValveProgramWindow
from Devices.connectionpy import connection_sensor
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


class Ui_SensorSettingsWindow(object):

    db = None
    actualRoomID = 0
    actualRoomName = ""
    configuration = None
    roomDataConfiguration = None
    
    def initDB(self, db):
        self.db = db

    def on_PB_goBack_clicked(self):
        self.close()
        self.sensorSettingsWindow = QtWidgets.QMainWindow()
        self.uiSensorValveProgramWindow = sensorValveProgramWindow.Ui_SensorValveProgramWindow()
        self.uiSensorValveProgramWindow.setupUi(self.sensorSettingsWindow, self.db, self.actualRoomID, self.actualRoomName)
        self.sensorSettingsWindow.showMaximized()

    def on_PB_connectSensor_pressed(self):
        self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
            "SensorSettingsWindow", "Connecting..."))
    
    def on_PB_connectSensor_released(self):
        sensorID = self.LE_sensor.text()

        if (sensorID == "" or not(str(sensorID).isdecimal())):
            print("Sensor ID empty or non numerical!")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Insert a valid numerical-only ID")
            msg.setWindowTitle("Error")
            msg.exec_()
            self.PB_connectSensor.setEnabled(True)
            self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Add Sensor..."))

        else: # ID sensore inserito

                        # Check se ID attuatore già presente
            flag = 0
            actualNumSensors = len(self.roomDataConfiguration["conf"][self.actualRoomID]["sensors"])
            for i in range(0, actualNumSensors):
                if (str(sensorID).lower() == str(self.roomDataConfiguration["conf"][self.actualRoomID]["sensors"][i]["sensorID"]).lower()):
                    flag = 1
                    break
            if (flag == 1): # L'ID Attuatore esiste già, ritorna errore
                print("ID Sensors already IN!")
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText(
                    "This sensor has been already connected!")
                msg.setWindowTitle("Error")
                msg.exec_()
                self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
            "SensorSettingsWindow", "Add"))
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
                returnID = connection_sensor.connection(sensorID, net_SSID, net_PWD, str(self.actualRoomName) + str(self.actualRoomID))    
                # returnID = 0
                if (returnID == 0):
                    print("OK! Sensor is being connected!")

                    if (len(self.roomDataConfiguration["conf"][self.actualRoomID]["sensors"]) == 1 and str(self.roomDataConfiguration["conf"][self.actualRoomID]["sensors"][0]["sensorID"]) == ""):
                        self.roomDataConfiguration["conf"][self.actualRoomID]["sensors"][0]["sensorID"] = sensorID
                    else:
                        self.roomDataConfiguration["conf"][self.actualRoomID]["sensors"].append({"sensorID" : sensorID})

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setInformativeText(
                        "Sensor connected!")
                    msg.setWindowTitle("Connected!")
                    msg.exec_()

                    database_manager.update_roomData_configuration(self.db, self.roomDataConfiguration)
                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Connect"))

                elif (returnID == -1):
                    print("Sensor not found in BT proximity, check actuator ID pliz")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Sensor ID not found, please retry")
                    msg.setWindowTitle("Errore")
                    msg.exec_()
                    
                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Not connected!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -2):
                    print("Cannot connect, Bluetooth Socket error.")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Actuator not connected, error in BT socket")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Not connected!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -3):
                    print("Nothing received from sensor, did you pushed the button?")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Push the sensor button BEFORE the connection attempt!")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Not connected!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -4):
                    print("Cannot connect, no transmission from sensor")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "No transmission from the sensor")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Not connected!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -5):
                    print("Cannot connect, error transmitting SSID")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Error while transferring the SSID to the sensor")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Not connected!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -6):
                    print("Cannot connect, error transmitting WIFI Password")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Error while tansferring the network password to the senosr")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Not connected!"))
                    self.PB_connectSensor.setEnabled(True)

                # elif (returnID == -7):
                #     print("Cannot connect, error transmitting MQTT Info")

                #     msg = QtWidgets.QMessageBox()
                #     msg.setIcon(QtWidgets.QMessageBox.Critical)
                #     msg.setInformativeText(
                #         "Errore nella trasmissione delle info MQTT al sensore")
                #     msg.setWindowTitle("Error")
                #     msg.exec_()

                #     self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                #             "SensorSettingsWindow", "Not connected!"))
                #     self.PB_connectSensor.setEnabled(True)

                elif (returnID == -8):
                    print("Cannot connect, error transmitting room name Info")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Error while transferring MQTT info to the sensor")
                    msg.setWindowTitle("Error")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Not connected!"))
                    self.PB_connectSensor.setEnabled(True)

    def on_PB_deleteSensor_clicked(self):
        sensorID = self.LE_sensor.text()

        if (sensorID == "" or not(str(sensorID).isdecimal())):
            print("Sensor ID empty or non numerical!")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Insert a valid numerical-only ID")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        else: # ID sensore inserito correttamente
            # Cerca il sensore, se esiste eliminalo
            flag = 0
            actualNumSensors = len(self.roomDataConfiguration["conf"][self.actualRoomID]["sensors"])
            for i in range(0, actualNumSensors):
                if (str(sensorID).lower() == str(self.roomDataConfiguration["conf"][self.actualRoomID]["sensors"][i]["sensorID"]).lower()):
                    del self.roomDataConfiguration["conf"][self.actualRoomID]["sensors"][i]
                    flag = 1
                    break
                    
            if (flag == 1):
                database_manager.update_roomData_configuration(self.db, self.roomDataConfiguration)
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setInformativeText(
                    "Sensor deleted!\nYou will no more receive data from it.")
                msg.setWindowTitle("Info")
                msg.exec_()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText(
                    "Error! Sensor not found!")
                msg.setWindowTitle("Error")
                msg.exec_()


    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_connectSensor.pressed.connect(self.on_PB_connectSensor_pressed)
        self.PB_connectSensor.released.connect(self.on_PB_connectSensor_released)
        self.PB_deleteSensor.clicked.connect(self.on_PB_deleteSensor_clicked)

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
        self.sensorSettingsWindow.close()

    def reloadRoomData(self):
        self.configuration = database_manager.get_configuration(self.db)
        self.roomDataConfiguration = database_manager.get_roomData_configuration(self.db)

    def setupUi(self, SensorSettingsWindow, db, actualRoomID, actualRoomName):

        self.sensorSettingsWindow = SensorSettingsWindow
        self.sensorSettingsWindow.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)

        SensorSettingsWindow.setObjectName("SensorSettingsWindow")
        SensorSettingsWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(10)
        SensorSettingsWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(SensorSettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(677, 0, 121, 61))
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
        self.PB_goBack.setGeometry(QtCore.QRect(0, 380, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_goBack.setFont(font)
        self.PB_goBack.setObjectName("PB_goBack")
        self.LE_sensor = MyQLineEdit(self.centralwidget)
        self.LE_sensor.setGeometry(QtCore.QRect(170, 200, 531, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LE_sensor.setFont(font)
        self.LE_sensor.setObjectName("LE_sensor")        
        self.label_SensorSettings = QtWidgets.QLabel(self.centralwidget)
        self.label_SensorSettings.setGeometry(QtCore.QRect(-10, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_SensorSettings.setFont(font)
        self.label_SensorSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_SensorSettings.setObjectName("label_SensorSettings")
        self.label_SensorID = QtWidgets.QLabel(self.centralwidget)
        self.label_SensorID.setGeometry(QtCore.QRect(150, 150, 140, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_SensorID.setFont(font)
        self.label_SensorID.setAlignment(QtCore.Qt.AlignCenter)
        self.label_SensorID.setObjectName("label_SensorID")
        self.PB_connectSensor = QtWidgets.QPushButton(self.centralwidget)
        self.PB_connectSensor.setGeometry(QtCore.QRect(170, 310, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_connectSensor.setFont(font)
        self.PB_connectSensor.setObjectName("PB_connectSensor")
        self.label_RoomName = QtWidgets.QLabel(self.centralwidget)
        self.label_RoomName.setGeometry(QtCore.QRect(200, 80, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_RoomName.setFont(font)
        self.label_RoomName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_RoomName.setObjectName("label_RoomName")
        self.PB_deleteSensor = QtWidgets.QPushButton(self.centralwidget)
        self.PB_deleteSensor.setGeometry(QtCore.QRect(470, 310, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_deleteSensor.setFont(font)
        self.PB_deleteSensor.setObjectName("PB_deleteSensor")
        SensorSettingsWindow.setCentralWidget(self.centralwidget)

        self.initDB(db)
        self.reloadRoomData()
        self.actualRoomID = actualRoomID
        self.actualRoomName = actualRoomName

        self.timer = QTimer()

        self.activeFunctionsConnection()

        self.retranslateUi(SensorSettingsWindow)

    def retranslateUi(self, SensorSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SensorSettingsWindow.setWindowTitle(
            _translate("SensorSettingsWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(
            _translate("SensorSettingsWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate(
            "SensorSettingsWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("SensorSettingsWindow", "<"))
        self.LE_sensor.setPlaceholderText(_translate("SensorSettingsWindow", "Insert sensor ID"))
        self.label_SensorSettings.setText(_translate("SensorSettingsWindow", "Sensor\n"
                                                     "Settings"))
        self.label_SensorID.setText(_translate(
            "SensorSettingsWindow", "Sensor ID:"))
        self.PB_connectSensor.setText(
            _translate("SensorSettingsWindow", "Add"))
        self.label_RoomName.setText(_translate(
            "SensorSettingsWindow", "Actual Room: " + str(self.actualRoomName)))
        self.PB_deleteSensor.setText(
            _translate("SensorSettingsWindow", "Delete"))
