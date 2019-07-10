import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import sensorValveProgramWindow
from Devices.connectionpy import connection_sensor
import data


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


class Ui_SensorSettingsWindow(object):

    db = None
    actualRoomID = 0
    actualRoomName = ""
    
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
            "SensorSettingsWindow", "Sto connettendo..."))
    
    def on_PB_connectSensor_released(self):
        self.PB_connectSensor.setEnabled(False)
        sensorID = self.LE_sensor.text()

        if (sensorID == ""):
            print("Sensor ID cannot be empty!")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Inserire un ID sensore, ID obbligatorio")
            msg.setWindowTitle("Errore")
            msg.exec_()
            self.PB_connectSensor.setEnabled(True)
            self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Add Sensor..."))

        else: # ID sensore inserito
            net_SSID = data.networkData["net_SSID"]
            net_PWD = data.networkData["net_PWD"]

            if (net_SSID == "" or net_PWD == ""):
                print("Net SSID and NET PWD cannot be empty! Maybe Raspone is not connected to network...")

                print("No SSID and PWD found when connecting actuator")
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText(
                    "Connettere il termostato al WiFi di casa prima di aggiungere un Sensore!")
                msg.setWindowTitle("Errore")
                msg.exec_()

            else: 
                
                returnID = connection_sensor.connection(sensorID, net_SSID, net_PWD, self.actualRoomName)    
                if (returnID == 0):
                    print("OK! Actuator is being connected!")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setInformativeText(
                        "Sensore collegato!")
                    msg.setWindowTitle("Connesso!")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Connesso!"))
                    self.PB_connectSensor.setEnabled(False)

                elif (returnID == -1):
                    print("Actuator not found in BT proximity, check actuator ID pliz")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "ID Sensore non trovato, riprovare")
                    msg.setWindowTitle("Errore")
                    msg.exec_()
                    
                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Non connesso, riprovare...!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -2):
                    print("Cannot connect, Bluetooth Socket error.")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Sensore non connesso, errore nel socket BT")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Non connesso, riprovare...!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -3):
                    print("Nothing received from sensor, did you pushed the button?")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Premere il tasto sul sensore PRIMA del tentativo di connessione")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Non connesso, riprovare...!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -4):
                    print("Cannot connect, no transmission from sensor")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Nessuna trasmissione dal sensore")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Non connesso, riprovare...!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -5):
                    print("Cannot connect, error transmitting SSID")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Errore nella trasmissione del SSID di rete al sensore")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Non connesso, riprovare...!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -6):
                    print("Cannot connect, error transmitting WIFI Password")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Errore nella trasmissione della password di rete al sensore")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Non connesso, riprovare...!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -7):
                    print("Cannot connect, error transmitting MQTT Info")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Errore nella trasmissione delle info MQTT al sensore")
                    msg.setWindowTitle("Error")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Non connesso, riprovare...!"))
                    self.PB_connectSensor.setEnabled(True)

                elif (returnID == -8):
                    print("Cannot connect, error transmitting room name Info")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Errore nella trasmissione del nome della stanza al sensore")
                    msg.setWindowTitle("Error")
                    msg.exec_()

                    self.PB_connectSensor.setText(QtCore.QCoreApplication.translate(
                            "SensorSettingsWindow", "Non connesso, riprovare...!"))
                    self.PB_connectSensor.setEnabled(True)

    # TODO: Aggiungere metodo per l'eliminazione del sensore
    # Decidere se mostrare una lista all'utente che dovrà poi selezionare il nome del sensore da 
    # eliminare. Oppure chiedere all'utente di specificare il nome del sensore e fare il check 
    # che tale sensore esista veramente --> strada più easy
    def on_PB_deleteSensor_clicked(self):
        pass

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
        self.sensorSettingsWindow.close()

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
        self.LE_sensor = QtWidgets.QLineEdit(self.centralwidget)
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
        self.LE_sensor.setPlaceholderText(_translate("SensorSettingsWindow", "Inserire identificativo del sensore"))
        self.label_SensorSettings.setText(_translate("SensorSettingsWindow", "Sensor\n"
                                                     "Settings"))
        self.label_SensorID.setText(_translate(
            "SensorSettingsWindow", "Sensor ID:"))
        self.PB_connectSensor.setText(
            _translate("SensorSettingsWindow", "Aggiungi"))
        self.label_RoomName.setText(_translate(
            "SensorSettingsWindow", "Actual Room: " + str(self.actualRoomName)))
        self.PB_deleteSensor.setText(
            _translate("SensorSettingsWindow", "Elimina"))
