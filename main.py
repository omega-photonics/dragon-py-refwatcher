#!/usr/bin/python

import sys
from PyQt4 import QtGui
from mainwindow import MainWindow
import model

def main(connect):
    settings = model.Model()
    app = QtGui.QApplication(sys.argv)
    wnd = MainWindow(settings=settings, connect=connect)
    wnd.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    connect = '-nodev' not in sys.argv
    main(connect)
