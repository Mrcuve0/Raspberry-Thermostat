from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import mainWindow
import networkSettingsWindow
import addRoomWindow
import deleteRoomWindow
import addActuatorWindow
import deleteActuatorWindow


class Ui_SettingsWindow(object):

    db = None

    def initDB(self, db):
        self.db = db

    def on_PB_goBack_clicked(self):
        self.close()
        self.settingsWindow = QtWidgets.QMainWindow()
        self.uiMainWindow = mainWindow.Ui_MainWindow()
        self.uiMainWindow.setupUi(self.settingsWindow, self.db, 0)
        self.settingsWindow.showMaximized()

    def on_PB_network_clicked(self):
        self.close()
        self.settingsWindow = QtWidgets.QMainWindow()
        self.uiNetworkSettingsWindow = networkSettingsWindow.Ui_NetworkSettingsWindow()
        self.uiNetworkSettingsWindow.setupUi(self.settingsWindow, self.db)
        self.settingsWindow.showMaximized()

    def on_PB_AddRoom_clicked(self):
        self.close()
        self.settingsWindow = QtWidgets.QMainWindow()
        self.uiAddRoomWindow = addRoomWindow.Ui_addRoomWindow()
        self.uiAddRoomWindow.setupUi(self.settingsWindow, self.db)
        self.settingsWindow.showMaximized()

    def on_PB_DeleteRoom_clicked(self):
        self.close()
        self.settingsWindow = QtWidgets.QMainWindow()
        self.uiDeleteRoomWindow = deleteRoomWindow.Ui_deleteRoomWindow()
        self.uiDeleteRoomWindow.setupUi(self.settingsWindow, self.db)
        self.settingsWindow.showMaximized()

    def on_PB_AddActuator_clicked(self):
        self.close()
        self.settingsWindow = QtWidgets.QMainWindow()
        self.uiAddActuatorWindow = addActuatorWindow.Ui_addActuatorWindow()
        self.uiAddActuatorWindow.setupUi(self.settingsWindow, self.db)
        self.settingsWindow.showMaximized()

    def on_PB_DeleteActuator_clicked(self):
        self.close()
        self.settingsWindow = QtWidgets.QMainWindow()
        self.uiDeleteActuatorWindow = deleteActuatorWindow.Ui_deleteActuatorWindow()
        self.uiDeleteActuatorWindow.setupUi(self.settingsWindow, self.db)
        self.settingsWindow.showMaximized()

    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_network.clicked.connect(self.on_PB_network_clicked)
        self.PB_AddRoom.clicked.connect(self.on_PB_AddRoom_clicked)
        self.PB_DeleteRoom.clicked.connect(self.on_PB_DeleteRoom_clicked)
        self.PB_AddActuator.clicked.connect(self.on_PB_AddActuator_clicked)
        self.PB_DeleteActuator.clicked.connect(self.on_PB_DeleteActuator_clicked)
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
        self.settingsWindow.close()

    def setupUi(self, SettingsWindow, db):

        self.settingsWindow = SettingsWindow
        self.settingsWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(800, 480)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
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
        self.PB_network = QtWidgets.QPushButton(self.centralwidget)
        self.PB_network.setGeometry(QtCore.QRect(180, 80, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_network.setFont(font)
        self.PB_network.setObjectName("PB_network")
        self.PB_AddRoom = QtWidgets.QPushButton(self.centralwidget)
        self.PB_AddRoom.setGeometry(QtCore.QRect(180, 160, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_AddRoom.setFont(font)
        self.PB_AddRoom.setObjectName("PB_AddRoom")
        self.PB_AddActuator = QtWidgets.QPushButton(self.centralwidget)
        self.PB_AddActuator.setGeometry(QtCore.QRect(180, 240, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_AddActuator.setFont(font)
        self.PB_AddActuator.setObjectName("PB_AddActuator")
        self.PB_DeleteRoom = QtWidgets.QPushButton(self.centralwidget)
        self.PB_DeleteRoom.setGeometry(QtCore.QRect(480, 160, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_DeleteRoom.setFont(font)
        self.PB_DeleteRoom.setObjectName("PB_DeleteRoom")
        self.PB_DeleteActuator = QtWidgets.QPushButton(self.centralwidget)
        self.PB_DeleteActuator.setGeometry(QtCore.QRect(480, 240, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_DeleteActuator.setFont(font)
        self.PB_DeleteActuator.setObjectName("PB_DeleteActuator")
        SettingsWindow.setCentralWidget(self.centralwidget)

        self.timer = QTimer()

        self.initDB(db)

        self.activeFunctionsConnection()
        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(_translate("SettingsWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate("SettingsWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("SettingsWindow", "<"))
        self.PB_network.setText(_translate("SettingsWindow", "Network"))
        self.PB_AddRoom.setText(_translate("SettingsWindow", "Add Room"))
        self.PB_AddActuator.setText(_translate("SettingsWindow", "Add Actuator"))
        self.PB_DeleteRoom.setText(_translate("SettingsWindow", "Delete Room"))
        self.PB_DeleteActuator.setText(_translate("SettingsWindow", "Delete Actuator"))
