#!/usr/bin/python3
from PyQt5 import QtWidgets, QtCore
from sys import argv, exit, stdout

from source.aaa import MainWindow

if __name__ == "__main__":

    QtCore.QCoreApplication.setOrganizationName("Intes corporation")
    QtCore.QCoreApplication.setApplicationName("KNPN")

    application = QtWidgets.QApplication(argv)
    window = MainWindow()
    window.show()
    exit(application.exec_())
    application.exit()
