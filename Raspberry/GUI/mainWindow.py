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

# TODO: Gestionedelle stanze:
# 1) TESTARE! --> Scorrere la stanza cliccando i pulsanti, mostrare la stanza giusta nel placeholder
# 3) Quando si aggiunge una stanza si aggiunge un elemento all'interno di configuration
# Questo va gestito correttamente in ogni tasto di questa finestra (increase, decrease ecc)
# Magari passare come parametro l'ID della stanza (che sarà incrementale) che ovviamente 
# si riferirà alla stanza attualmente visualizzata nel placeholder. (la temperatura se 
# incrementata va associata alla stanza giusta)
# 4) Passare alla roomSettings il DB


class Ui_MainWindow(object):

    db = None
    configuration = None
    newConfiguration = None

    roomTemp = 0.0
    newRoomTemp = 0.0
    repetitions = 0
    actualRoomID = 0

    season = None # can be "hot" or "cold"
    mode = None # can be "manual", "antifreeze" or "programmable"

    def initDB(self, db):
        self.db = db

    def on_PB_tempIncrease_pressed(self):
        print("Incremento temperatura")
        self.timerUpdateTemp.stop()
        self.timerSetTemp.start(5000)

        if (self.repetitions == 0):
            # Quale è stata l'ultima temperatura impostata per questa stanza?
            # Uso questa temperature come base di partenza per poi decrementarla
            self.configuration = database_manager.get_configuration(self.db)
            self.roomTemp = self.configuration["rooms_settings"][self.actualRoomID]["info"]["temp"]
        
        print("OLD temp value: " + str(self.roomTemp))
        self.roomTemp = self.roomTemp + 0.5   
        self.newRoomTemp = self.roomTemp
        print("NEW temp: " + str(self.newRoomTemp))
        self.LCDTempSet.display(self.newRoomTemp)

        self.repetitions = self.repetitions + 1

    def on_PB_tempDecrease_pressed(self):

        print("Decremento temperatura")
        self.timerUpdateTemp.stop()
        self.timerSetTemp.start(5000)

        if (self.repetitions == 0):
            # Quale è stata l'ultima temperatura impostata per questa stanza?
            # Uso questa temperature come base di partenza per poi decrementarla
            self.configuration = database_manager.get_configuration(self.db)
            self.roomTemp = self.configuration["rooms_settings"][self.actualRoomID]["info"]["temp"]
        
        print("OLD temp value: " + str(self.roomTemp))
        self.roomTemp = self.roomTemp - 0.5   
        self.newRoomTemp = self.roomTemp
        print("NEW temp: " + str(self.newRoomTemp))
        self.LCDTempSet.display(self.newRoomTemp)

        self.repetitions = self.repetitions + 1

    # Season
    def on_PB_winter_pressed(self):
        self.season = "cold"
        self.newConfiguration = self.configuration
        self.newConfiguration["rooms_settings"][self.actualRoomID]["season"] = self.season
        database_manager.update_configuration(self.db, self.newConfiguration)

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setUnderline(True)
        self.PB_winter.setFont(font)

        font.setUnderline(False)
        self.PB_summer.setFont(font)
        # self.PB_winter.setEnabled(False)
        # self.PB_summer.setEnabled(True)

    def on_PB_summer_pressed(self):
        self.season = "hot"
        self.newConfiguration = self.configuration
        self.newConfiguration["rooms_settings"][self.actualRoomID]["season"] = self.season
        database_manager.update_configuration(self.db, self.newConfiguration)

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setUnderline(True)
        self.PB_summer.setFont(font)

        font.setUnderline(False)
        self.PB_winter.setFont(font)
        # self.PB_summer.setEnabled(False)
        # self.PB_winter.setEnabled(True)
        
    # Mode
    def on_PB_program_pressed(self):
        self.mode = "program"
        self.newConfiguration = self.configuration
        self.newConfiguration["rooms_settings"][self.actualRoomID]["mode"] = self.mode
        database_manager.update_configuration(self.db, self.newConfiguration)

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

    def on_PB_manual_pressed(self):
        self.mode = "manual"
        self.newConfiguration = self.configuration
        self.newConfiguration["rooms_settings"][self.actualRoomID]["mode"] = self.mode
        database_manager.update_configuration(self.db, self.newConfiguration)

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

    def on_PB_antiFreeze_pressed(self):
        self.mode = "antifreeze"
        self.newConfiguration = self.configuration
        self.newConfiguration["rooms_settings"][self.actualRoomID]["mode"] = self.mode
        database_manager.update_configuration(self.db, self.newConfiguration)

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
        # TODO: La temperatura dell'Antifreeze è 15?
        self.LCDTempSet.display(15.0)

    def disableProgramAntiFreezeButtons(self):
        # Se è in modalità programma/antifreeze alcuni tasti devono essere disabilitati
        self.PB_tempIncrease.setDisabled(True)
        self.PB_tempDecrease.setDisabled(True)
        self.LCDTempSet.setDisabled(True)

    def enableManualButtons(self):
        # Se è in modalità manuale alcuni tasti devono essere abilitati
        self.PB_tempIncrease.setDisabled(False)
        self.PB_tempDecrease.setDisabled(False)
        self.LCDTempSet.setDisabled(False)

    def on_PB_roomList_clicked(self):
        self.close()
        self.mainWindow = QtWidgets.QMainWindow()
        self.uiSensorValveProgramWindow = sensorValveProgramWindow.Ui_SensorValveProgramWindow()
        self.uiSensorValveProgramWindow.setupUi(self.mainWindow, self.db, self.actualRoomID, self.configuration["rooms_settings"][self.actualRoomID]["room_name"])
        self.mainWindow.showMaximized()

    def on_PB_nextRoom_clicked(self):
        if (self.actualRoomID < len(self.configuration["rooms_settings"]) - 1):    # Posso scorrere ancora
            self.actualRoomID = self.actualRoomID + 1
        self.reloadRoomData()

    def on_PB_prevRoom_clicked(self):   
        if (self.actualRoomID > 0):    # Posso scorrere ancora
            self.actualRoomID = self.actualRoomID - 1
        self.reloadRoomData()
        
    def reloadRoomData(self):
        self.configuration = database_manager.get_configuration(self.db)
        self.roomTemp = self.configuration["rooms_settings"][self.actualRoomID]["info"]["temp"]
        self.season = self.configuration["rooms_settings"][self.actualRoomID]["season"]
        self.mode = self.configuration["rooms_settings"][self.actualRoomID]["mode"]

        if (self.mode == "program"):
            self.on_PB_program_pressed()
            self.disableProgramAntiFreezeButtons()

        elif (self.mode == "manual"):
            self.on_PB_manual_pressed()
            self.enableManualButtons()

        else:
            self.on_PB_antiFreeze_pressed()
            self.disableProgramAntiFreezeButtons()
            # TODO: La temperatura dell'Antifreeze è 15?
            self.LCDTempSet.display(15.0)

        if (self.season == "cold"):
            self.on_PB_winter_pressed()
        else:
            self.on_PB_summer_pressed()

        self.PB_roomList.setText(QtCore.QCoreApplication.translate("MainWindow", "Actual Room: " + str(self.configuration["rooms_settings"][self.actualRoomID]["room_name"])))
    
    def on_PB_settings_clicked(self):
        self.close()
        self.mainWindow = QtWidgets.QMainWindow()
        self.uiSettingsWindow = settingsWindow.Ui_SettingsWindow()
        self.uiSettingsWindow.setupUi(self.mainWindow, self.db)
        self.mainWindow.showMaximized()

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

        #PB_RoomList
        self.PB_roomList.clicked.connect(self.on_PB_roomList_clicked)
        self.PB_nextRoom.clicked.connect(self.on_PB_nextRoom_clicked)
        self.PB_prevRoom.clicked.connect(self.on_PB_prevRoom_clicked)

        # Timer for date and time updating
        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)

        # Timer for actual temperature updating
        self.timerUpdateTemp.timeout.connect(self.updateTempData)
        # TODO: Decidere
        # impostato a 1 sec, impostare a 1 minuto?
        self.timerUpdateTemp.start(2000)

        # Timer for set temperature confirmation
        self.timerSetTemp.timeout.connect(self.commitSetTempData)

        # Init funcs
        self.updateTempData()

        # La prima stanza è sempre quella principale dove è il raspone
        # Sarà poi l'utente a selezionare le altre stanze
        self.actualRoomID = 0
        self.reloadRoomData()
        
    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def updateTempData(self):
        # TODO: Uncomment
        # lastTemperatures is a list
        # lastTemperatures = database_manager.get_last_temperatures(self.db)

        self.configuration = database_manager.get_configuration(self.db)
        self.roomSetTemp = self.configuration["rooms_settings"][self.actualRoomID]["info"]["temp"]

        if (self.mode != "antifreeze"):
            self.LCDTempSet.display(self.roomSetTemp)

        lastTemperatures = []
        lastTemperatures.append(18.5)
        lastTemperatures.append(20.2)
        # print(str(lastTemperatures))
        
        if (len(lastTemperatures) > 0):
            self.LCDTempAct.display(lastTemperatures.pop())
        else:
            self.LCDTempAct.display(0.0)

    def commitSetTempData(self):
        print("\t --> COMMIT of new temperature")
        self.timerUpdateTemp.start(1000)
        self.timerSetTemp.stop()

        self.repetitions = 0

        self.newConfiguration = self.configuration
        self.newConfiguration["rooms_settings"][0]["info"]["temp"] = self.newRoomTemp

        database_manager.update_configuration(self.db, self.configuration)

    def close(self):
        self.mainWindow.close()

    def initLoadData(self):
        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, './../netCredentials.json')

        with open(filename, 'r') as json_file:  
            # json.dump(my_details, json_file)
            data.networkData = json.load(json_file)

    def setupUi(self, MainWindow, db):

        self.mainWindow = MainWindow
        self.mainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)

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
        self.PB_program.setGeometry(QtCore.QRect(130, 320, 81, 61))
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
        self.PB_manual.setGeometry(QtCore.QRect(220, 320, 81, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_manual.setFont(font)
        self.PB_manual.setFlat(False)
        self.PB_manual.setObjectName("PB_manual")
        self.PB_winter = QtWidgets.QPushButton(self.centralwidget)
        self.PB_winter.setGeometry(QtCore.QRect(440, 320, 111, 61))
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
        self.PB_onOff = QtWidgets.QPushButton(self.centralwidget)
        self.PB_onOff.setGeometry(QtCore.QRect(0, 300, 111, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_onOff.setFont(font)
        self.PB_onOff.setObjectName("PB_onOff")
        self.PB_roomList = QtWidgets.QPushButton(self.centralwidget)
        self.PB_roomList.setGeometry(QtCore.QRect(80, 393, 641, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_roomList.setFont(font)
        self.PB_roomList.setObjectName("PB_roomList")
        self.PB_prevRoom = QtWidgets.QPushButton(self.centralwidget)
        self.PB_prevRoom.setGeometry(QtCore.QRect(0, 393, 81, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_prevRoom.setFont(font)
        self.PB_prevRoom.setObjectName("PB_prevRoom")
        self.PB_nextRoom = QtWidgets.QPushButton(self.centralwidget)
        self.PB_nextRoom.setGeometry(QtCore.QRect(720, 393, 81, 61))
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
        self.PB_summer.setGeometry(QtCore.QRect(560, 320, 111, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_summer.setFont(font)
        self.PB_summer.setFlat(False)
        self.PB_summer.setObjectName("PB_summer")
        self.PB_antiFreeze = QtWidgets.QPushButton(self.centralwidget)
        self.PB_antiFreeze.setGeometry(QtCore.QRect(310, 320, 91, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_antiFreeze.setFont(font)
        self.PB_antiFreeze.setFlat(False)
        self.PB_antiFreeze.setObjectName("PB_antiFreeze")
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
        self.PB_onOff.raise_()
        self.PB_roomList.raise_()
        self.PB_prevRoom.raise_()
        self.PB_nextRoom.raise_()
        self.labelTempAct.raise_()
        self.labelTempSet.raise_()
        self.PB_summer.raise_()
        self.PB_antiFreeze.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.initDB(db)

        self.timer = QTimer()
        self.timerUpdateTemp = QTimer()
        self.timerSetTemp = QTimer()

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
        self.PB_onOff.setText(_translate("MainWindow", "On/Off"))
        self.PB_prevRoom.setText(_translate("MainWindow", "<"))
        self.PB_nextRoom.setText(_translate("MainWindow", ">"))
        self.labelTempAct.setText(_translate("MainWindow", "Actual temperature:"))
        self.labelTempSet.setText(_translate("MainWindow", "Temperature set: "))
        self.PB_summer.setText(_translate("MainWindow", "Summer"))
        self.PB_antiFreeze.setText(_translate("MainWindow", "AntiF"))

