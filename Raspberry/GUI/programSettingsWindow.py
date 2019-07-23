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

import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import sensorValveProgramWindow
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

class Ui_ProgramSettingsWindow(object):

    db = None
    configuration = None
    newConfiguration = None

    actualRoomIndex = 0
    actualRoomID = 0
    actualRoomName = ""

    def initDB(self, db):
        self.db = db

    
    def searchActualRoomID(self):
        self.configuration = database_manager.get_configuration(self.db)

        self.actualRoomID = self.configuration["rooms_settings"][self.actualRoomIndex]["room"]

    def loadScreenData(self):
        self.configuration = database_manager.get_configuration(self.db)
        if (self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFM"] != "" and \
            self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFE"] != "" and \
            self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFN"] != "" and \
            self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEM"] != "" and \
            self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEE"] != "" and \
            self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEN"] != ""):
                self.LE_MFM.setText(str(self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFM"]))
                self.LE_MFE.setText(str(self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFE"]))
                self.LE_MFN.setText(str(self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["MFN"]))
                self.LE_WEM.setText(str(self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEM"]))
                self.LE_WEE.setText(str(self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEE"]))
                self.LE_WEN.setText(str(self.configuration["rooms_settings"][self.actualRoomIndex]["program"]["WEN"]))

    def on_PB_goBack_clicked(self):
        self.close()
        self.programSettingsWindow = QtWidgets.QMainWindow()
        self.uiSensorValveProgramWindow = sensorValveProgramWindow.Ui_SensorValveProgramWindow()
        self.uiSensorValveProgramWindow.setupUi(self.programSettingsWindow, self.db, self.actualRoomIndex, self.actualRoomName)
        self.programSettingsWindow.showMaximized()

    def on_PB_apply_clicked(self):
        # Check if chars different than numbers have been inserted
        if (not(self.LE_MFE.text().isdecimal() and self.LE_MFM.text().isdecimal() and self.LE_MFN.text().isdecimal() and self.LE_WEE.text().isdecimal() and self.LE_WEM.text().isdecimal() and self.LE_WEN.text().isdecimal())):
            # Errore, c'è almeno un campo o vuoto o contenente valor non numnerici
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "You cannot submit empty or non-numerical forms!")
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            self.configuration = database_manager.get_configuration(self.db)
            self.newConfiguration = self.configuration
            # self.newConfiguration["rooms_settings"][self.actualRoomIndex]["program"] = {"temp": {"MFM" : self.LE_MFM.text(), "MFE" : self.LE_MFE.text(), "MFN" : self.LE_MFN.text(), "WEM" : self.LE_WEM.text(), "WEE" : self.LE_WEE.text(), "WEN" : self.LE_WEN.text()}}
            self.newConfiguration["rooms_settings"][self.actualRoomIndex]["program"]["MFM"] = int(self.LE_MFM.text())
            self.newConfiguration["rooms_settings"][self.actualRoomIndex]["program"]["MFE"] = int(self.LE_MFE.text())
            self.newConfiguration["rooms_settings"][self.actualRoomIndex]["program"]["MFN"] = int(self.LE_MFN.text())
            self.newConfiguration["rooms_settings"][self.actualRoomIndex]["program"]["WEM"] = int(self.LE_WEM.text())
            self.newConfiguration["rooms_settings"][self.actualRoomIndex]["program"]["WEE"] = int(self.LE_WEE.text())
            self.newConfiguration["rooms_settings"][self.actualRoomIndex]["program"]["WEN"] = int(self.LE_WEN.text())

            database_manager.update_configuration(self.db, self.newConfiguration)

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setInformativeText(
                "Program updated correctly!")
            msg.setWindowTitle("Info")
            msg.exec_()  

    def on_PB_clearAll_clicked(self):
        self.LE_MFE.setText("")
        self.LE_MFM.setText("")
        self.LE_MFN.setText("")
        self.LE_WEE.setText("")
        self.LE_WEM.setText("")
        self.LE_WEN.setText("")

    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)
        self.PB_clearAll.clicked.connect(self.on_PB_clearAll_clicked)
        self.PB_apply.clicked.connect(self.on_PB_apply_clicked)

        self.loadScreenData()

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
        self.programSettingsWindow.close()

    def setupUi(self, ProgramSettingsWindow, db, actualRoomIndex, actualRoomName):

        self.programSettingsWindow = ProgramSettingsWindow
        self.programSettingsWindow.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)

        font = QtGui.QFont()
        font.setPointSize(10)
        ProgramSettingsWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(ProgramSettingsWindow)
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
        self.label_ValveSettings = QtWidgets.QLabel(self.centralwidget)
        self.label_ValveSettings.setGeometry(QtCore.QRect(-10, 0, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_ValveSettings.setFont(font)
        self.label_ValveSettings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ValveSettings.setObjectName("label_ValveSettings")
        self.PB_apply = QtWidgets.QPushButton(self.centralwidget)
        self.PB_apply.setGeometry(QtCore.QRect(520, 380, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_apply.setFont(font)
        self.PB_apply.setObjectName("PB_apply")
        self.label_ValveName = QtWidgets.QLabel(self.centralwidget)
        self.label_ValveName.setGeometry(QtCore.QRect(-60, 60, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_ValveName.setFont(font)
        self.label_ValveName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ValveName.setObjectName("label_ValveName")
        self.PB_clearAll = QtWidgets.QPushButton(self.centralwidget)
        self.PB_clearAll.setGeometry(QtCore.QRect(180, 380, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_clearAll.setFont(font)
        self.PB_clearAll.setObjectName("PB_clearAll")
        self.labelMorning = QtWidgets.QLabel(self.centralwidget)
        self.labelMorning.setGeometry(QtCore.QRect(190, 140, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelMorning.setFont(font)
        self.labelMorning.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMorning.setObjectName("labelMorning")
        self.labelEvening = QtWidgets.QLabel(self.centralwidget)
        self.labelEvening.setGeometry(QtCore.QRect(190, 190, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelEvening.setFont(font)
        self.labelEvening.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEvening.setObjectName("labelEvening")
        self.labelNight = QtWidgets.QLabel(self.centralwidget)
        self.labelNight.setGeometry(QtCore.QRect(190, 240, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelNight.setFont(font)
        self.labelNight.setAlignment(QtCore.Qt.AlignCenter)
        self.labelNight.setObjectName("labelNight")
        self.labelMonFri = QtWidgets.QLabel(self.centralwidget)
        self.labelMonFri.setGeometry(QtCore.QRect(340, 100, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelMonFri.setFont(font)
        self.labelMonFri.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMonFri.setObjectName("labelMonFri")
        self.labelWeekend = QtWidgets.QLabel(self.centralwidget)
        self.labelWeekend.setGeometry(QtCore.QRect(570, 100, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelWeekend.setFont(font)
        self.labelWeekend.setAlignment(QtCore.Qt.AlignCenter)
        self.labelWeekend.setObjectName("labelWeekend")
        self.LE_MFM = MyQLineEdit(self.centralwidget)
        self.LE_MFM.setGeometry(QtCore.QRect(360, 140, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LE_MFM.setFont(font)
        self.LE_MFM.setAlignment(QtCore.Qt.AlignCenter)
        self.LE_MFM.setObjectName("LE_MFM")
        self.LE_MFE = MyQLineEdit(self.centralwidget)
        self.LE_MFE.setGeometry(QtCore.QRect(360, 190, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LE_MFE.setFont(font)
        self.LE_MFE.setAlignment(QtCore.Qt.AlignCenter)
        self.LE_MFE.setObjectName("LE_MFE")
        self.LE_MFN = MyQLineEdit(self.centralwidget)
        self.LE_MFN.setGeometry(QtCore.QRect(360, 240, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LE_MFN.setFont(font)
        self.LE_MFN.setAlignment(QtCore.Qt.AlignCenter)
        self.LE_MFN.setObjectName("LE_MFN")
        self.LE_WEE = MyQLineEdit(self.centralwidget)
        self.LE_WEE.setGeometry(QtCore.QRect(600, 190, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LE_WEE.setFont(font)
        self.LE_WEE.setAlignment(QtCore.Qt.AlignCenter)
        self.LE_WEE.setObjectName("LE_WEE")
        self.LE_WEN = MyQLineEdit(self.centralwidget)
        self.LE_WEN.setGeometry(QtCore.QRect(600, 240, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LE_WEN.setFont(font)
        self.LE_WEN.setAlignment(QtCore.Qt.AlignCenter)
        self.LE_WEN.setObjectName("LE_WEN")
        self.LE_WEM = MyQLineEdit(self.centralwidget)
        self.LE_WEM.setGeometry(QtCore.QRect(600, 140, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LE_WEM.setFont(font)
        self.LE_WEM.setAlignment(QtCore.Qt.AlignCenter)
        self.LE_WEM.setObjectName("LE_WEM")
        ProgramSettingsWindow.setCentralWidget(self.centralwidget)

        self.initDB(db)
        self.actualRoomIndex = actualRoomIndex
        self.actualRoomName = actualRoomName

        self.searchActualRoomID()

        self.timer = QTimer()

        self.activeFunctionsConnection()

        self.retranslateUi(ProgramSettingsWindow)

    def retranslateUi(self, ProgramSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        ProgramSettingsWindow.setWindowTitle(_translate("ProgramSettingsWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(_translate("ProgramSettingsWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate("ProgramSettingsWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("ProgramSettingsWindow", "<"))
        self.label_ValveSettings.setText(_translate("ProgramSettingsWindow", "Program\n"
"Settings"))
        self.PB_apply.setText(_translate("ProgramSettingsWindow", "Apply"))
        self.label_ValveName.setText(_translate("ProgramSettingsWindow", "Actual Room: " + str(self.actualRoomName)))
        self.PB_clearAll.setText(_translate("ProgramSettingsWindow", "Clear all"))
        self.labelMorning.setText(_translate("ProgramSettingsWindow", "06:00 - 12:00"))
        self.labelEvening.setText(_translate("ProgramSettingsWindow", "12:00 - 24:00"))
        self.labelNight.setText(_translate("ProgramSettingsWindow", "24:00 - 06:00"))
        self.labelMonFri.setText(_translate("ProgramSettingsWindow", "Monday - Friday"))
        self.labelWeekend.setText(_translate("ProgramSettingsWindow", "Weekend"))
        self.LE_MFM.setPlaceholderText(_translate("ProgramSettingsWindow", "°C"))
        self.LE_MFE.setPlaceholderText(_translate("ProgramSettingsWindow", "°C"))
        self.LE_MFN.setPlaceholderText(_translate("ProgramSettingsWindow", "°C"))
        self.LE_WEE.setPlaceholderText(_translate("ProgramSettingsWindow", "°C"))
        self.LE_WEN.setPlaceholderText(_translate("ProgramSettingsWindow", "°C"))
        self.LE_WEM.setPlaceholderText(_translate("ProgramSettingsWindow", "°C"))
