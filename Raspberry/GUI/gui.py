import mainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

import os
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

# Importa classe definita con QTDesigner
# from mainWindow import Ui_MainWindow


class MainWindow(QMainWindow, mainWindow.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    raspyGUI = MainWindow()
    raspyGUI.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
