import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import sensorValveProgramWindow
from Devices.connectionpy import connection_sensor
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


class Ui_ValveSettingsWindow(object):

    db = None
    configuration = None
    roomDataConfiguration = None
    actualRoomID = 0
    actualRoomName = ""

    def initDB(self, db):
        self.db = db

    
    def reloadRoomData(self):
        self.configuration = database_manager.get_configuration(self.db)
        self.roomDataConfiguration = database_manager.get_roomData_configuration(self.db)

    def on_PB_goBack_clicked(self):
        self.close()
        self.valveSettingsWindow = QtWidgets.QMainWindow()
        self.uiSensorValveProgramWindow = sensorValveProgramWindow.Ui_SensorValveProgramWindow()
        self.uiSensorValveProgramWindow.setupUi(self.valveSettingsWindow, self.db, self.actualRoomID, self.actualRoomName)
        self.valveSettingsWindow.showMaximized()

    # TODO: Aggiungere metodo per la connessione della valvola
    def on_PB_connectValve_clicked(self):

        self.roomDataConfiguration = database_manager.get_roomData_configuration(self.db)
        actuatorID = self.LE_actuator.text()
        valveID = self.LE_valve.text()
        if (actuatorID == "" or valveID == ""):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Actuator ID and Valve ID cannot be empty!")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        numActuators
        self.roomDataConfiguration["conf"][self.actualRoomID]["actuators"][]
        pass

    # TODO: Aggiungere metodo per l'eliminazione della valvola
    def on_PB_deleteValve_clicked(self):
        pass

    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_connectValve.clicked.connect(self.on_PB_connectValve_clicked)
        self.PB_deleteValve.clicked.connect(self.on_PB_deleteValve_clicked)
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
        self.valveSettingsWindow.close()

    def setupUi(self, ValveSettingsWindow, db, actualRoomID, actualRoomName):

        self.valveSettingsWindow = ValveSettingsWindow
        self.valveSettingsWindow.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)

        ValveSettingsWindow.setObjectName("ValveSettingsWindow")
        ValveSettingsWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(10)
        ValveSettingsWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(ValveSettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
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
        self.PB_goBack = QtWidgets.QPushButton(self.centralwidget)
        self.PB_goBack.setGeometry(QtCore.QRect(0, 380, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_goBack.setFont(font)
        self.PB_goBack.setObjectName("PB_goBack")
        self.label_ValveSettings = QtWidgets.QLabel(self.centralwidget)
        self.label_ValveSettings.setGeometry(QtCore.QRect(-10, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_ValveSettings.setFont(font)
        self.label_ValveSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ValveSettings.setObjectName("label_ValveSettings")
        self.label_ValveID = QtWidgets.QLabel(self.centralwidget)
        self.label_ValveID.setGeometry(QtCore.QRect(120, 190, 140, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_ValveID.setFont(font)
        self.label_ValveID.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ValveID.setObjectName("label_ValveID")
        self.PB_connectValve = QtWidgets.QPushButton(self.centralwidget)
        self.PB_connectValve.setGeometry(QtCore.QRect(170, 330, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_connectValve.setFont(font)
        self.PB_connectValve.setObjectName("PB_connectValve")
        self.label_RoomName = QtWidgets.QLabel(self.centralwidget)
        self.label_RoomName.setGeometry(QtCore.QRect(230, 60, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_RoomName.setFont(font)
        self.label_RoomName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_RoomName.setObjectName("label_RoomName")
        self.PB_deleteValve = QtWidgets.QPushButton(self.centralwidget)
        self.PB_deleteValve.setGeometry(QtCore.QRect(470, 330, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_deleteValve.setFont(font)
        self.PB_deleteValve.setObjectName("PB_deleteValve")
        self.label_ActuatorID = QtWidgets.QLabel(self.centralwidget)
        self.label_ActuatorID.setGeometry(QtCore.QRect(140, 90, 140, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_ActuatorID.setFont(font)
        self.label_ActuatorID.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ActuatorID.setObjectName("label_ActuatorID")
        self.LE_actuator = QtWidgets.QLineEdit(self.centralwidget)
        self.LE_actuator.setGeometry(QtCore.QRect(140, 140, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LE_actuator.setFont(font)
        self.LE_actuator.setObjectName("LE_actuator")
        self.LE_valve = QtWidgets.QLineEdit(self.centralwidget)
        self.LE_valve.setGeometry(QtCore.QRect(140, 240, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LE_valve.setFont(font)
        self.LE_valve.setObjectName("LE_valve")
        ValveSettingsWindow.setCentralWidget(self.centralwidget)

        self.initDB(db)
        self.actualRoomID = actualRoomID
        self.actualRoomName = actualRoomName

        self.reloadRoomData()

        self.timer = QTimer()

        self.activeFunctionsConnection()
        self.retranslateUi(ValveSettingsWindow)

    def retranslateUi(self, ValveSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        ValveSettingsWindow.setWindowTitle(_translate("ValveSettingsWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(_translate("ValveSettingsWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate("ValveSettingsWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("ValveSettingsWindow", "<"))
        self.label_ValveSettings.setText(_translate("ValveSettingsWindow", "Valve\n"
"Settings"))
        self.label_ValveID.setText(_translate("ValveSettingsWindow", "Valve ID:"))
        self.PB_connectValve.setText(_translate("ValveSettingsWindow", "Add"))
        self.label_RoomName.setText(_translate("ValveSettingsWindow", "Actual Room: " + str(self.actualRoomName)))
        self.PB_deleteValve.setText(_translate("ValveSettingsWindow", "Delete"))
        self.label_ActuatorID.setText(_translate("ValveSettingsWindow", "Actuator ID:"))
        self.LE_actuator.setPlaceholderText(_translate("ValveSettingsWindow", "Insert Actuator ID"))
        self.LE_valve.setPlaceholderText(_translate("ValveSettingsWindow", "Insert Valve ID"))
