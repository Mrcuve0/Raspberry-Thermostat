import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

import mainWindow
import BlankBGWindow

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

# Importa classe definita con QTDesigner
# from mainWindow import Ui_MainWindow


class MainWindow(QMainWindow, mainWindow.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


class BlankWindow(QMainWindow, BlankBGWindow.Ui_BlankWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    blank = BlankWindow()
    blank.showMaximized()
    raspyGUI = MainWindow()
    raspyGUI.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
