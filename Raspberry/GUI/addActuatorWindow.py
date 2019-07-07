import sys
import subprocess

print(sys.path[0])  # <->/Raspberry-Thermostat/Raspberry/GUI
sys.path.insert(0, sys.path[0] + "/../../") # /Raspberry-Thermostat/
print(sys.path)


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import settingsWindow
from Devices.connectionpy import connection_actuator
import networkConnection
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


class Ui_addActuatorWindow(object):

    def on_PB_goBack_clicked(self):
        self.close()
        self.addActuatorWindow = QtWidgets.QMainWindow()
        self.uiSettingsWindow = settingsWindow.Ui_SettingsWindow()
        self.uiSettingsWindow.setupUi(self.addActuatorWindow)
        self.addActuatorWindow.showMaximized()

    def on_PB_addActuator_pressed(self):
        self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
            "AddActuatorWindow", "Sto connettendo..."))

    # TODO: Aggiungo l'attuatore alla lista di attuatori già inseriti nel sistema
    # Ritorna un errore se un attuatore è già presente con lo stesso nome nella lista
    def on_PB_addActuator_released(self):
        self.PB_addActuator.setEnabled(False)
        actuatorID = self.LE_actuator.text()

        if (actuatorID == ""):
            print("Actuator ID cannot be empty!")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Inserire un ID attuatore, ID obbligatorio")
            msg.setWindowTitle("Errore")
            msg.exec_()

        else: # ID attuatore inserito
            net_SSID = data.networkData["net_SSID"]
            net_PWD = data.networkData["net_PWD"]

            if (net_SSID == "" or net_PWD == ""):
                print("Net SSID and NET PWD cannot be empty! Maybe Raspone is not connected to network...")

                print("No SSID and PWD found when connecting actuator")
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText(
                    "Connettere il termostato al WiFi di casa prima di aggiungere un attuatore!")
                msg.setWindowTitle("Errore")
                msg.exec_()

            else: 
                returnID = connection_actuator.connection(actuatorID, net_SSID, net_PWD)    
                if (returnID == 0):
                    print("OK! Actuator is being connected!")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setInformativeText(
                        "Attuatore collegato!")
                    msg.setWindowTitle("Connesso!")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Connesso!"))
                    self.PB_addActuator.setEnabled(False)

                elif (returnID == -1):
                    print("Actuator not found in BT proximity, check actuator ID pliz")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "ID Attuatore non trovato, riprovare")
                    msg.setWindowTitle("Errore")
                    msg.exec_()
                    
                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Non connesso, riprovare...!"))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -2):
                    print("Cannot connect, Bluetooth Socket error.")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Attuatore non connesso, errore nel socket BT")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Non connesso, riprovare...!"))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -3):
                    print("Nothing received from actuator, did you pushed the button?")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Premere il tasto sull'attuatore PRIMA del tentativo di connessione")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Non connesso, riprovare...!"))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -4):
                    print("Cannot connect, no transmission from actuator")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Nessuna trasmissione dall'attuatore")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Non connesso, riprovare...!"))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -5):
                    print("Cannot connect, error transmitting SSID")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Errore nella trasmissione del SSID di rete all'attuatore")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Non connesso, riprovare...!"))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -6):
                    print("Cannot connect, error transmitting WIFI Password")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Errore nella trasmissione della password di rete all'attuatore")
                    msg.setWindowTitle("Errore")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Non connesso, riprovare...!"))
                    self.PB_addActuator.setEnabled(True)

                elif (returnID == -7):
                    print("Cannot connect, error transmitting MQTT Info")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setInformativeText(
                        "Errore nella trasmissione delle info MQTT all'attuatore")
                    msg.setWindowTitle("Error")
                    msg.exec_()

                    self.PB_addActuator.setText(QtCore.QCoreApplication.translate(
                            "AddActuatorWindow", "Non connesso, riprovare...!"))
                    self.PB_addActuator.setEnabled(True)

        
        
    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_addActuator.pressed.connect(self.on_PB_addActuator_pressed)
        self.PB_addActuator.released.connect(self.on_PB_addActuator_released)
        self.LE_actuator.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)

    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def close(self):
        self.actuatorWindow.close()

    def setupUi(self, addActuatorWindow):
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
        self.PB_goBack.setGeometry(QtCore.QRect(0, 350, 111, 100))
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
        self.statusbar = QtWidgets.QStatusBar(addActuatorWindow)
        self.statusbar.setObjectName("statusbar")
        addActuatorWindow.setStatusBar(self.statusbar)

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
            "AddActuatorWindow", "Inserire ID dell'attuatore"))

        self.label_ActuatorSettings.setText(_translate("AddActuatorWindow", "Actuator\n"
                                                   "Settings"))
        self.label_ActuatorName.setText(_translate(
            "AddActuatorWindow", "Actuator Name:"))

        self.PB_addActuator.setText(_translate(
            "AddActuatorWindow", "Add Actuator..."))
