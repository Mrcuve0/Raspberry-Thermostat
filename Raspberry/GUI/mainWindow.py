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

import sys
import os
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import settingsWindow
import addRoomWindow
import sensorValveProgramWindow
import data

from database_manager import database_manager


class Ui_MainWindow(object):

    db = None
    configuration = None
    newConfiguration = None
    lastTemperatures = None

    roomTempSet = 0.0
    roomTempProgram = 0.0
    repetitions = 0

    actualRoomIndex = 0
    actualRoomID = 0

    season = "" # can be "hot" or "cold"
    mode = "" # can be "manual", "antifreeze", "programmable"
    weekend = 0 # Can be 0 or 1
    lastModifiedBy = "WEB"

    def initDB(self, db):
        self.db = db

    def searchActualRoomID(self):
        self.configuration = database_manager.get_configuration(self.db)

        self.actualRoomID = self.configuration["rooms_settings"][self.actualRoomIndex]["room"]

        # actualNumRooms = len(self.configuration["rooms_settings"])
        # for i in range(0, actualNumRooms):
        #     if (self.actualRoomID == self.configuration["rooms_settings"][i]["room"]):
        #         self.actualRoomIndex = i
        #         break

    # Season
    def on_PB_winter_pressed(self):
        self.season = "cold"
        self.lastModifiedBy = "GUI"
        self.updateScreenData()

    def on_PB_summer_pressed(self):
        self.season = "hot"
        self.lastModifiedBy = "GUI"
        self.updateScreenData()

    # Mode
    def on_PB_program_pressed(self):
        self.mode = "programmable"
        self.lastModifiedBy = "GUI"
        self.lastModifiedBy = "GUI"
        self.updateScreenData()

    def on_PB_manual_pressed(self):
        self.mode = "manual"
        self.lastModifiedBy = "GUI"
        self.updateScreenData()

    def on_PB_antiFreeze_pressed(self):
        self.mode = "antifreeze"
        self.lastModifiedBy = "GUI"
        self.updateScreenData()

    def on_PB_weekend_pressed(self):
        if (self.weekend == 0):
            self.weekend = 1
        elif (self.weekend == 1):
            self.weekend = 0

        self.lastModifiedBy = "GUI"
        self.updateScreenData()

    def disableProgramAntiFreezeButtons(self):
        # Se è in modalità programma/antifreeze alcuni tasti devono essere disabilitati
        self.PB_tempIncrease.setDisabled(True)
        self.PB_tempDecrease.setDisabled(True)
        self.LCDTempSet.setDisabled(True)
        self.PB_weekend.setDisabled(True)

    def enableManualButtons(self):
        # Se è in modalità manuale alcuni tasti devono essere abilitati
        self.PB_tempIncrease.setDisabled(False)
        self.PB_tempDecrease.setDisabled(False)
        self.LCDTempSet.setDisabled(False)
        self.PB_weekend.setDisabled(False)

    # Signals
    def on_PB_roomList_clicked(self):
        self.close()
        self.mainWindow = QtWidgets.QMainWindow()
        self.uiSensorValveProgramWindow = sensorValveProgramWindow.Ui_SensorValveProgramWindow()
        self.uiSensorValveProgramWindow.setupUi(self.mainWindow, self.db, self.actualRoomIndex, self.configuration["rooms_settings"][self.actualRoomIndex]["room_name"])
        self.mainWindow.showMaximized()

    def on_PB_nextRoom_clicked(self):
        if (self.actualRoomIndex < len(self.configuration["rooms_settings"]) - 1):    # Posso scorrere ancora
            self.actualRoomIndex = self.actualRoomIndex + 1

        self.actualRoomID = int(self.configuration["rooms_settings"][self.actualRoomIndex]["room"])
        self.lastModifiedBy = "WEB"
        self.updateScreenData()

    def on_PB_prevRoom_clicked(self):
        if (self.actualRoomIndex > 0):    # Posso scorrere ancora
            self.actualRoomIndex = self.actualRoomIndex - 1

        self.actualRoomID = int(self.configuration["rooms_settings"][self.actualRoomIndex]["room"])
        self.lastModifiedBy = "WEB"
        self.updateScreenData()

    def on_PB_settings_clicked(self):
        self.close()
        self.mainWindow = QtWidgets.QMainWindow()
        self.uiSettingsWindow = settingsWindow.Ui_SettingsWindow()
        self.uiSettingsWindow.setupUi(self.mainWindow, self.db)
        self.mainWindow.showMaximized()

    def on_PB_tempIncrease_pressed(self):
        print("Incremento temperatura")

        self.lastModifiedBy = "GUI"

        print("OLD temp value: " + str(self.roomTempSet))
        self.roomTempSet = self.roomTempSet + 0.5
        print("NEW temp: " + str(self.roomTempSet))
        self.updateScreenData()

    def on_PB_tempDecrease_pressed(self):

        print("Decremento temperatura")

        self.lastModifiedBy = "GUI"

        print("OLD temp value: " + str(self.roomTempSet))
        self.roomTempSet = self.roomTempSet - 0.5
        print("NEW temp: " + str(self.roomTempSet))
        self.updateScreenData()

    # Signals connection
    def activeFunctionsConnection(self):
        # PB_roomList
        self.PB_roomList.clicked.connect(self.on_PB_roomList_clicked)
        self.PB_settings.clicked.connect(self.on_PB_settings_clicked)

        # PB_Increase and PB_Decrease
        self.PB_tempDecrease.pressed.connect(self.on_PB_tempDecrease_pressed)
        self.PB_tempIncrease.pressed.connect(self.on_PB_tempIncrease_pressed)

        # PB_Season
        self.PB_winter.pressed.connect(self.on_PB_winter_pressed)
        self.PB_summer.pressed.connect(self.on_PB_summer_pressed)

        # PB_Mode
        self.PB_program.pressed.connect(self.on_PB_program_pressed)
        self.PB_manual.pressed.connect(self.on_PB_manual_pressed)
        self.PB_antiFreeze.pressed.connect(self.on_PB_antiFreeze_pressed)
        self.PB_weekend.pressed.connect(self.on_PB_weekend_pressed)

        #PB_RoomList
        self.PB_roomList.clicked.connect(self.on_PB_roomList_clicked)
        self.PB_nextRoom.clicked.connect(self.on_PB_nextRoom_clicked)
        self.PB_prevRoom.clicked.connect(self.on_PB_prevRoom_clicked)

        # Timer for date and time updating
        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)

        # Timer for actual temperature updating
        self.timerUpdateScreenData.timeout.connect(self.updateScreenData)
        self.timerUpdateScreenData.start(1000)

        # Init funcs
        self.updateScreenData()

    # Timer handlers
    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def updateScreenData(self):
        self.lastTemperatures = database_manager.get_last_temperatures(self.db)

        # Lettura delle impostazioni, se sono differenti con quelle precedenti
        # allora la configuration è stata cambiata dal sito e non dall'interfaccia
        self.configuration = database_manager.get_configuration(self.db)

        if (self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFM"] != "" and \
            self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFE"] != "" and \
            self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFN"] != "" and \
            self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEM"] != "" and \
            self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEE"] != "" and \
            self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEN"] != ""):
            # MONDAY - FRIDAY
            date = QDate.currentDate()
            time = QTime.currentTime()
            if (date.dayOfWeek() >= 1 and date.dayOfWeek() <= 5):
                if (time.hour() >= 6 and time.hour() < 12):
                    self.roomTempProgram = self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFM"]
                if (time.hour() >= 12 and time.hour() <= 23):
                    self.roomTempProgram = self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFE"]
                if (time.hour() >= 0  and time.hour() < 6):
                    self.roomTempProgram = self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFN"]

            # WEEKEND
            elif (date.dayOfWeek() >= 6 and date.dayOfWeek() <= 7):
                if (time.hour() >= 6 and time.hour() < 12):
                    self.roomTempProgram = self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEM"]
                if (time.hour() >= 12 and time.hour() <= 23):
                    self.roomTempProgram = self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEE"]
                if (time.hour() >= 0 and time.hour() < 6):
                    self.roomTempProgram = self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEN"]
        else:
            self.roomTempProgram = "00"

        if (self.lastModifiedBy == "GUI"):
            self.newConfiguration = self.configuration
            self.newConfiguration["rooms_settings"][self.actualRoomIndex]["info"]["temp"] = self.roomTempSet
            self.newConfiguration["rooms_settings"][self.actualRoomIndex]["season"] = self.season
            self.newConfiguration["rooms_settings"][self.actualRoomIndex]["mode"] = self.mode
            self.newConfiguration["rooms_settings"][self.actualRoomIndex]["info"]["weekend"] = self.weekend

            print("\t --> COMMIT: ")
            print("\t\tID: " + str(self.actualRoomID))
            print("\t\tTemp: " + str(self.roomTempSet))
            print("\t\tSeason: " + str(self.season))
            print("\t\tMode: " + str(self.mode))
            print("\t\tWeekend: " + str(self.weekend))

            database_manager.update_configuration(self.db, self.newConfiguration)
            self.lastModifiedBy = "WEB"

        else:   # WEB
            self.roomTempSet = self.configuration["rooms_settings"][self.actualRoomIndex]["info"]["temp"]
            self.season = self.configuration["rooms_settings"][self.actualRoomIndex]["season"]
            self.mode = self.configuration["rooms_settings"][self.actualRoomIndex]["mode"]
            self.weekend = self.configuration["rooms_settings"][self.actualRoomIndex]["info"]["weekend"]

        self.reloadRoomData()

        self.LCDTempAct.display(str("o"))
        for el in self.lastTemperatures:
            if (str(el["room"]) == str(self.actualRoomID)):
                self.LCDTempAct.display("%.1f" % round(el["temperature"], 1))
                break

    def commitSetTempData(self):
        print("\t --> COMMIT of new temperature")
        self.timerUpdateScreenData.start(1000)

        self.repetitions = 0

        self.newConfiguration = self.configuration
        self.newConfiguration["rooms_settings"][self.actualRoomID]["info"]["temp"] = self.roomTempSet

        database_manager.update_configuration(self.db, self.newConfiguration)

    def reloadRoomData(self):

        if (self.mode == "programmable"):
            # self.on_PB_program_pressed()
            font = QtGui.QFont()
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            font.setUnderline(True)
            self.PB_program.setFont(font)

            font.setUnderline(False)
            self.PB_manual.setFont(font)
            self.PB_antiFreeze.setFont(font)

            self.disableProgramAntiFreezeButtons()

            # Show temperature according to program
            self.LCDTempSet.display("%.1f" % round(float(self.roomTempProgram), 1))

        elif (self.mode == "manual"):
            # self.on_PB_manual_pressed()
            font = QtGui.QFont()
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            font.setUnderline(True)
            self.PB_manual.setFont(font)

            font.setUnderline(False)
            self.PB_program.setFont(font)
            self.PB_antiFreeze.setFont(font)

            self.enableManualButtons()

            if (self.weekend == 1):
                font = QtGui.QFont()
                font.setPointSize(16)
                font.setBold(True)
                font.setWeight(75)
                font.setUnderline(True)
                self.PB_weekend.setFont(font)
            else:
                font = QtGui.QFont()
                font.setPointSize(16)
                font.setBold(True)
                font.setWeight(75)
                font.setUnderline(False)
                self.PB_weekend.setFont(font)

            self.LCDTempSet.display("%.1f" % round(float(self.roomTempSet), 1))

        else:
            # self.on_PB_antiFreeze_pressed()
            font = QtGui.QFont()
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            font.setUnderline(True)
            self.PB_antiFreeze.setFont(font)

            font.setUnderline(False)
            self.PB_program.setFont(font)
            self.PB_manual.setFont(font)

            self.disableProgramAntiFreezeButtons()
            self.LCDTempSet.display("%.1f" % round(15.00, 1))

        if (self.season == "cold"):
            # self.on_PB_winter_pressed()
            font = QtGui.QFont()
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            font.setUnderline(True)
            self.PB_winter.setFont(font)

            font.setUnderline(False)
            self.PB_summer.setFont(font)

        else:
            # self.on_PB_summer_pressed()
            font = QtGui.QFont()
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            font.setUnderline(True)
            self.PB_summer.setFont(font)

            font.setUnderline(False)
            self.PB_winter.setFont(font)

        self.PB_roomList.setText(QtCore.QCoreApplication.translate("MainWindow", "Actual Room: " + str(self.configuration["rooms_settings"][self.actualRoomIndex]["room_name"])))

    # Window handling
    def close(self):
        self.timer.stop()
        # self.timerSetTemp.stop()
        self.timerUpdateScreenData.stop()
        self.mainWindow.close()

    def initLoadData(self):
        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, './../netCredentials.json')

        try:
            with open(filename, 'r') as json_file:
                data.networkData = json.load(json_file)
        except:
            pass

    def setupUi(self, MainWindow, db, actualRoomIndex):

        self.mainWindow = MainWindow
        self.mainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.PB_tempIncrease = QtWidgets.QPushButton(self.centralwidget)
        self.PB_tempIncrease.setGeometry(QtCore.QRect(689, 120, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_tempIncrease.setFont(font)
        self.PB_tempIncrease.setObjectName("PB_tempIncrease")
        self.PB_tempDecrease = QtWidgets.QPushButton(self.centralwidget)
        self.PB_tempDecrease.setGeometry(QtCore.QRect(690, 250, 111, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_tempDecrease.setFont(font)
        self.PB_tempDecrease.setObjectName("PB_tempDecrease")
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
        self.LCDTempSet = QtWidgets.QLCDNumber(self.centralwidget)
        self.LCDTempSet.setGeometry(QtCore.QRect(380, 160, 291, 151))
        self.LCDTempSet.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LCDTempSet.setSmallDecimalPoint(True)
        self.LCDTempSet.setDigitCount(4)
        self.LCDTempSet.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.LCDTempSet.setObjectName("LCDTempSet")
        self.PB_settings = QtWidgets.QPushButton(self.centralwidget)
        self.PB_settings.setGeometry(QtCore.QRect(0, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_settings.setFont(font)
        self.PB_settings.setObjectName("PB_settings")
        self.PB_program = QtWidgets.QPushButton(self.centralwidget)
        self.PB_program.setGeometry(QtCore.QRect(30, 340, 81, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_program.setFont(font)
        self.PB_program.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.PB_program.setAutoDefault(False)
        self.PB_program.setDefault(False)
        self.PB_program.setFlat(False)
        self.PB_program.setObjectName("PB_program")
        self.PB_manual = QtWidgets.QPushButton(self.centralwidget)
        self.PB_manual.setGeometry(QtCore.QRect(120, 340, 81, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_manual.setFont(font)
        self.PB_manual.setFlat(False)
        self.PB_manual.setObjectName("PB_manual")
        self.PB_winter = QtWidgets.QPushButton(self.centralwidget)
        self.PB_winter.setGeometry(QtCore.QRect(440, 340, 111, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.PB_winter.setFont(font)
        self.PB_winter.setFlat(False)
        self.PB_winter.setObjectName("PB_winter")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_roomList = QtWidgets.QPushButton(self.centralwidget)
        self.PB_roomList.setGeometry(QtCore.QRect(80, 420, 641, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_roomList.setFont(font)
        self.PB_roomList.setObjectName("PB_roomList")
        self.PB_prevRoom = QtWidgets.QPushButton(self.centralwidget)
        self.PB_prevRoom.setGeometry(QtCore.QRect(0, 420, 81, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_prevRoom.setFont(font)
        self.PB_prevRoom.setObjectName("PB_prevRoom")
        self.PB_nextRoom = QtWidgets.QPushButton(self.centralwidget)
        self.PB_nextRoom.setGeometry(QtCore.QRect(720, 420, 81, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_nextRoom.setFont(font)
        self.PB_nextRoom.setObjectName("PB_nextRoom")
        self.LCDTempAct = QtWidgets.QLCDNumber(self.centralwidget)
        self.LCDTempAct.setGeometry(QtCore.QRect(20, 120, 341, 191))
        self.LCDTempAct.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LCDTempAct.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LCDTempAct.setSmallDecimalPoint(True)
        self.LCDTempAct.setDigitCount(4)
        self.LCDTempAct.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.LCDTempAct.setProperty("value", 0.0)
        self.LCDTempAct.setProperty("intValue", 0)
        self.LCDTempAct.setObjectName("LCDTempAct")
        self.labelTempAct = QtWidgets.QLabel(self.centralwidget)
        self.labelTempAct.setGeometry(QtCore.QRect(20, 100, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelTempAct.setFont(font)
        self.labelTempAct.setObjectName("labelTempAct")
        self.labelTempSet = QtWidgets.QLabel(self.centralwidget)
        self.labelTempSet.setGeometry(QtCore.QRect(380, 110, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelTempSet.setFont(font)
        self.labelTempSet.setObjectName("labelTempSet")
        self.PB_summer = QtWidgets.QPushButton(self.centralwidget)
        self.PB_summer.setGeometry(QtCore.QRect(560, 340, 111, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_summer.setFont(font)
        self.PB_summer.setFlat(False)
        self.PB_summer.setObjectName("PB_summer")
        self.PB_antiFreeze = QtWidgets.QPushButton(self.centralwidget)
        self.PB_antiFreeze.setGeometry(QtCore.QRect(310, 340, 91, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_antiFreeze.setFont(font)
        self.PB_antiFreeze.setFlat(False)
        self.PB_antiFreeze.setObjectName("PB_antiFreeze")
        self.PB_weekend = QtWidgets.QPushButton(self.centralwidget)
        self.PB_weekend.setGeometry(QtCore.QRect(210, 340, 91, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_weekend.setFont(font)
        self.PB_weekend.setFlat(False)
        self.PB_weekend.setObjectName("PB_weekend")
        self.LCDTempAct.raise_()
        self.PB_tempIncrease.raise_()
        self.PB_tempDecrease.raise_()
        self.dateEdit.raise_()
        self.timeEdit.raise_()
        self.LCDTempSet.raise_()
        self.PB_settings.raise_()
        self.PB_program.raise_()
        self.PB_manual.raise_()
        self.PB_winter.raise_()
        self.PB_roomList.raise_()
        self.PB_prevRoom.raise_()
        self.PB_nextRoom.raise_()
        self.labelTempAct.raise_()
        self.labelTempSet.raise_()
        self.PB_summer.raise_()
        self.PB_antiFreeze.raise_()
        self.PB_weekend.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.initDB(db)
        self.actualRoomIndex = actualRoomIndex
        self.searchActualRoomID()

        self.timer = QTimer()
        self.timerUpdateScreenData = QTimer()

        self.activeFunctionsConnection()
        self.initLoadData()

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PB_tempIncrease.setText(_translate("MainWindow", "+"))
        self.PB_tempDecrease.setText(_translate("MainWindow", "-"))
        self.dateEdit.setDisplayFormat(_translate("MainWindow", "dd - MM - yyyy"))
        self.timeEdit.setDisplayFormat(_translate("MainWindow", "HH : mm"))
        self.PB_settings.setText(_translate("MainWindow", "Settings"))
        self.PB_program.setText(_translate("MainWindow", "P"))
        self.PB_manual.setText(_translate("MainWindow", "M"))
        self.PB_winter.setText(_translate("MainWindow", "Winter"))
        self.PB_prevRoom.setText(_translate("MainWindow", "<"))
        self.PB_nextRoom.setText(_translate("MainWindow", ">"))
        self.labelTempAct.setText(_translate("MainWindow", "Actual temperature:"))
        self.labelTempSet.setText(_translate("MainWindow", "Temperature set: "))
        self.PB_summer.setText(_translate("MainWindow", "Summer"))
        self.PB_antiFreeze.setText(_translate("MainWindow", "AntiF"))
        self.PB_weekend.setText(_translate("MainWindow", "WE"))
