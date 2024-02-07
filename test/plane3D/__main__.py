import sys
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

from _3d import *
from thread import *

if __name__ == "__main__":
    ######################################
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()

    myapp.show()
    ######################################
    thread = Thread()
    thread.new_record.connect(myapp._show)
    thread.start()
    sys.exit(app.exec_())
