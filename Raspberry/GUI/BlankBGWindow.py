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

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer


class Ui_BlankWindow(object):

    def activeFunctionsConnection(self):
        self.timer.timeout.connect(self.showTime)
        self.showTime()
        self.timer.start(1000)

    def showTime(self):
        date = QDate.currentDate()
        time = QTime.currentTime()
        self.timeEdit.setTime(time)
        self.dateEdit.setDate(date)

    def setupUi(self, BlankWindow):

        BlankWindow.setObjectName("BlankWindow")
        BlankWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        BlankWindow.resize(800, 480)
        self.centralwidget = QtWidgets.QWidget(BlankWindow)
        self.centralwidget.setObjectName("centralwidget")
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
        BlankWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(BlankWindow)
        self.statusbar.setObjectName("statusbar")
        BlankWindow.setStatusBar(self.statusbar)

        self.activeFunctionsConnection()
        self.retranslateUi(BlankWindow)
        QtCore.QMetaObject.connectSlotsByName(BlankWindow)

    def retranslateUi(self, BlankWindow):
        _translate = QtCore.QCoreApplication.translate
        BlankWindow.setWindowTitle(_translate("BlankWindow", "BlankWindow"))
        _translate = QtCore.QCoreApplication.translate
        self.dateEdit.setDisplayFormat(
            _translate("BlankWindow", "dd - MM - yyyy"))
        self.timeEdit.setDisplayFormat(_translate("BlankWindow", "HH : mm"))
