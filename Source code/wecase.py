#!/usr/bin/env pythoni
# coding=utf-8

# WeCase -- Linux Sina Weibo Client
# Since 4th,Feb,2013
# This is a TEST version
# Wait for ...

# Well, Let's go!


from PyQt4 import QtCore,QtGui
from ui.MainWindow import Ui_frm_MainWindow
import sys

class WeCaseWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_frm_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    wecasewin=WeCaseWindow()
    wecasewin.show()
    sys.exit(app.exec_())
