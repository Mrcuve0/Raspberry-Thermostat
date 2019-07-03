from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import sensorValveProgramWindow


class Ui_ProgramSettingsWindow(object):

    def on_PB_goBack_clicked(self):
        self.close()
        self.programSettingsWindow = QtWidgets.QMainWindow()
        self.uiSensorValveProgramWindow = sensorValveProgramWindow.Ui_SensorValveProgramWindow()
        self.uiSensorValveProgramWindow.setupUi(self.programSettingsWindow)
        self.programSettingsWindow.showMaximized()

    def activeFunctionsConnection(self):
        self.PB_goBack.clicked.connect(self.on_PB_goBack_clicked)

        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)

    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def close(self):
        self.programSettingsWindow.close()

    def setupUi(self, ProgramSettingsWindow):

        self.programSettingsWindow = ProgramSettingsWindow
        self.programSettingsWindow.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)

        ProgramSettingsWindow.setObjectName("ProgramSettingsWindow")
        ProgramSettingsWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(10)
        ProgramSettingsWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(ProgramSettingsWindow)
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
        self.label_ValveID.setGeometry(QtCore.QRect(150, 150, 140, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_ValveID.setFont(font)
        self.label_ValveID.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ValveID.setObjectName("label_ValveID")
        self.PB_connectValve = QtWidgets.QPushButton(self.centralwidget)
        self.PB_connectValve.setGeometry(QtCore.QRect(170, 310, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_connectValve.setFont(font)
        self.PB_connectValve.setObjectName("PB_connectValve")
        self.label_RoomName = QtWidgets.QLabel(self.centralwidget)
        self.label_RoomName.setGeometry(QtCore.QRect(200, 80, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_RoomName.setFont(font)
        self.label_RoomName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_RoomName.setObjectName("label_RoomName")
        self.PB_deleteValve = QtWidgets.QPushButton(self.centralwidget)
        self.PB_deleteValve.setGeometry(QtCore.QRect(470, 310, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_deleteValve.setFont(font)
        self.PB_deleteValve.setObjectName("PB_deleteValve")
        ProgramSettingsWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ProgramSettingsWindow)
        self.statusbar.setObjectName("statusbar")
        ProgramSettingsWindow.setStatusBar(self.statusbar)

        self.activeFunctionsConnection()
        self.retranslateUi(ProgramSettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(ProgramSettingsWindow)

    def retranslateUi(self, ProgramSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        ProgramSettingsWindow.setWindowTitle(
            _translate("ProgramSettingsWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(
            _translate("ProgramSettingsWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate(
            "ProgramSettingsWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("ProgramSettingsWindow", "<"))
        self.PT_sensor.setPlaceholderText(_translate(
            "ProgramSettingsWindow", "Inserire identificativo della valvola"))
        self.label_ValveSettings.setText(_translate("ProgramSettingsWindow", "Program\n"
                                                    "Settings"))
        self.label_ValveID.setText(_translate(
            "ProgramSettingsWindow", "Valve ID:"))
        self.PB_connectValve.setText(
            _translate("ProgramSettingsWindow", "Aggiungi"))
        self.label_RoomName.setText(_translate(
            "ProgramSettingsWindow", "<Room Name Here>"))
        self.PB_deleteValve.setText(
            _translate("ProgramSettingsWindow", "Elimina"))
