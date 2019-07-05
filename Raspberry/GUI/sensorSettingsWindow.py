import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import sensorValveProgramWindow
from Devices.connectionpy import connection_sensor


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

    def on_PB_goBack_clicked(self):
        self.close()
        self.sensorSettingsWindow = QtWidgets.QMainWindow()
        self.uiSensorValveProgramWindow = sensorValveProgramWindow.Ui_SensorValveProgramWindow()
        self.uiSensorValveProgramWindow.setupUi(self.sensorSettingsWindow)
        self.sensorSettingsWindow.showMaximized()

    # TODO: Aggiungere metodo per la connessione del sensore
    def on_PB_connectSensor_clicked(self):
        connection_sensor.connection()

    # TODO: Aggiungere metodo per l'eliminazione del sensore
    def on_PB_deleteSensor_clicked(self):
        pass

    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_connectSensor.clicked.connect(self.on_PB_connectSensor_clicked)
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

    def setupUi(self, SensorSettingsWindow):

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
        self.PT_sensor = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.PT_sensor.setGeometry(QtCore.QRect(170, 200, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PT_sensor.setFont(font)
        self.PT_sensor.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PT_sensor.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.PT_sensor.setOverwriteMode(True)
        self.PT_sensor.setObjectName("PT_sensor")
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
        self.statusbar = QtWidgets.QStatusBar(SensorSettingsWindow)
        self.statusbar.setObjectName("statusbar")
        SensorSettingsWindow.setStatusBar(self.statusbar)

        self.activeFunctionsConnection()
        self.retranslateUi(SensorSettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SensorSettingsWindow)

    def retranslateUi(self, SensorSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SensorSettingsWindow.setWindowTitle(
            _translate("SensorSettingsWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(
            _translate("SensorSettingsWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate(
            "SensorSettingsWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("SensorSettingsWindow", "<"))
        self.PT_sensor.setPlaceholderText(_translate(
            "SensorSettingsWindow", "Inserire identificativo del sensore"))
        self.label_SensorSettings.setText(_translate("SensorSettingsWindow", "Sensor\n"
                                                     "Settings"))
        self.label_SensorID.setText(_translate(
            "SensorSettingsWindow", "Sensor ID:"))
        self.PB_connectSensor.setText(
            _translate("SensorSettingsWindow", "Aggiungi"))
        self.label_RoomName.setText(_translate(
            "SensorSettingsWindow", "<Room Name Here>"))
        self.PB_deleteSensor.setText(
            _translate("SensorSettingsWindow", "Elimina"))
