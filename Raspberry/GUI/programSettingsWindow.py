from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer

import sensorValveProgramWindow


class Ui_ProgramSettingsWindow(object):

    db = None
    configuration = None
    newConfiguration = None

    actualRoomID = 0
    actualRoomName = ""

    def initDB(self, db):
        self.db = db

    def on_PB_goBack_clicked(self):
        self.close()
        self.programSettingsWindow = QtWidgets.QMainWindow()
        self.uiSensorValveProgramWindow = sensorValveProgramWindow.Ui_SensorValveProgramWindow()
        self.uiSensorValveProgramWindow.setupUi(self.programSettingsWindow, self.db, self.actualRoomID, self.actualRoomName)
        self.programSettingsWindow.showMaximized()

    # TODO: Complete apply button action
    def on_PB_apply_clicked(self):
        pass

    # TODO: Complete clearAll button action
    def on_PB_clearAll_clicked(self):
        pass

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

    def setupUi(self, ProgramSettingsWindow, db, actualRoomID, actualRoomName):

        self.programSettingsWindow = ProgramSettingsWindow
        self.programSettingsWindow.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)

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
        self.PB_apply = QtWidgets.QPushButton(self.centralwidget)
        self.PB_apply.setGeometry(QtCore.QRect(520, 380, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PB_apply.setFont(font)
        self.PB_apply.setObjectName("PB_apply")
        self.label_ValveName = QtWidgets.QLabel(self.centralwidget)
        self.label_ValveName.setGeometry(QtCore.QRect(210, 50, 361, 61))
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
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(50, 110, 701, 241))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget.setFont(font)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(70)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        ProgramSettingsWindow.setCentralWidget(self.centralwidget)

        self.initDB(db)
        self.actualRoomID = actualRoomID
        self.actualRoomName = actualRoomName

        self.timer = QTimer()

        self.activeFunctionsConnection()

        self.retranslateUi(ProgramSettingsWindow)

    def retranslateUi(self, ProgramSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        ProgramSettingsWindow.setWindowTitle(_translate("ProgramSettingsWindow", "MainWindow"))
        self.timeEdit.setDisplayFormat(_translate("ProgramSettingsWindow", "HH : mm"))
        self.dateEdit.setDisplayFormat(_translate("ProgramSettingsWindow", "dd - MM - yyyy"))
        self.PB_goBack.setText(_translate("ProgramSettingsWindow", "<"))
        self.label_ValveSettings.setText(_translate("ProgramSettingsWindow", "Sensor\n"
"Settings"))
        self.PB_apply.setText(_translate("ProgramSettingsWindow", "Apply"))
        self.label_ValveName.setText(_translate("ProgramSettingsWindow", "Actual Room: " + str(self.actualRoomName)))
        self.PB_clearAll.setText(_translate("ProgramSettingsWindow", "Clear all"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("ProgramSettingsWindow", "06:00 - 12:00"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("ProgramSettingsWindow", "12:00 - 24:00"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("ProgramSettingsWindow", "24:00 - 06:00"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ProgramSettingsWindow", "Monday - Friday"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ProgramSettingsWindow", "Weekend"))
