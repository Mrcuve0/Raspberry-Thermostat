import sys
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import settingsWindow
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


class Ui_addRoomWindow(object):

    db = None
    configuration = None
    newConfiguration = None

    actualNumRooms = 0

    def initDB(self, db):
        self.db = db

    def reloadRoomData(self):
        self.configuration = database_manager.get_configuration(self.db)

    def on_PB_goBack_clicked(self):
        self.close()
        self.roomWindow = QtWidgets.QMainWindow()
        self.uiSettingsWindow = settingsWindow.Ui_SettingsWindow()
        self.uiSettingsWindow.setupUi(self.roomWindow, self.db)
        self.roomWindow.showMaximized()

    # TODO: Aggiungo la stanza alla lista di stanze già disponibili nel sistema
    # Ritorna un errore se una stanza è già presente con lo stesso nome nella lista
    def on_PB_addRoom_clicked(self):
        self.actualNumRooms = len(self.configuration["rooms_settings"])
        roomName = self.LE_room.text()
        if (roomName == ""):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Room name cannot be empty!")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        # Aggiungi stanza alla configurazione
        # FIXME: la chiave room che tipo di dato vuole? 
        # Per ora gli passo il nome della stanza, ma è ridondante con la chiave 
        # "room_name"
        self.configuration["rooms_settings"].append({"room" : self.actualNumRooms, "room_name" : roomName, "mode" : "manual", "info" : {"temp" : 25, "weekend" : 0}, "season" : "hot"})

        self.newConfiguration = self.configuration
        database_manager.update_configuration(self.db, self.newConfiguration)

        print("\t --> COMMIT: Stanza aggiunta")
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setInformativeText(
            "Room added!")
        msg.setWindowTitle("Info")
        msg.exec_()
          
    def __handleTextChanged(self, text):
        if not self.LE_room.hasFocus:
            self.LE_room._beforeRoomName = text

    def __handleEditingFinished(self):
        beforeRoomName, afterRoomName = self.LE_room._beforeRoomName, self.LE_room.text()
        if beforeRoomName != afterRoomName:
            self.LE_room._beforeRoomName = afterRoomName
            self.LE_room.textChanged.emit(afterRoomName)
            self.PB_addRoom.setText(QtCore.QCoreApplication.translate(
                "AddRoomWindow", "Add Room"))
            self.PB_addRoom.setEnabled(True)
        
    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_addRoom.clicked.connect(self.on_PB_addRoom_clicked)
        self.LE_room.setFocusPolicy(QtCore.Qt.StrongFocus)

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
        self.roomWindow.close()

    def setupUi(self, addRoomWindow, db):
        self.roomWindow = addRoomWindow
        self.roomWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        addRoomWindow.setObjectName("AddRoomWindow")
        addRoomWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(10)
        addRoomWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(addRoomWindow)
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
        self.LE_room = MyQLineEdit(self.centralwidget)
        self.LE_room.setGeometry(QtCore.QRect(110, 130, 581, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LE_room.setFont(font)
        self.LE_room.setObjectName("LE_room")

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.label_RoomSettings = QtWidgets.QLabel(self.centralwidget)
        self.label_RoomSettings.setGeometry(QtCore.QRect(-10, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_RoomSettings.setFont(font)
        self.label_RoomSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_RoomSettings.setObjectName("label_RoomSettings")
        self.label_RoomName = QtWidgets.QLabel(self.centralwidget)
        self.label_RoomName.setGeometry(QtCore.QRect(90, 80, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_RoomName.setFont(font)
        self.label_RoomName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_RoomName.setObjectName("label_RoomName")

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.PB_addRoom = QtWidgets.QPushButton(self.centralwidget)
        self.PB_addRoom.setGeometry(QtCore.QRect(220, 240, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_addRoom.setFont(font)
        self.PB_addRoom.setObjectName("PB_addRoom")
        addRoomWindow.setCentralWidget(self.centralwidget)

        self.initDB(db)

        self.activeFunctionsConnection()
        self.retranslateUi(addRoomWindow)

    def retranslateUi(self, addRoomWindow):
        _translate = QtCore.QCoreApplication.translate
        addRoomWindow.setWindowTitle(
            _translate("AddRoomWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(
            _translate("AddRoomWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate(
            "AddRoomWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("AddRoomWindow", "<"))
        self.LE_room.setPlaceholderText(_translate(
            "AddRoomWindow", "Insert room name"))

        self.label_RoomSettings.setText(_translate("AddRoomWindow", "Room\n"
                                                   "Settings"))
        self.label_RoomName.setText(_translate(
            "AddRoomWindow", "Room Name:"))

        self.PB_addRoom.setText(_translate(
            "AddRoomWindow", "Add Room..."))
