# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/SmileyWindow.ui'
#
# Created: Sun Apr  7 21:18:44 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SmileyWindow(object):
    def setupUi(self, SmileyWindow):
        SmileyWindow.setObjectName(_fromUtf8("SmileyWindow"))
        SmileyWindow.resize(483, 285)
        self.gridLayout = QtGui.QGridLayout(SmileyWindow)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.smileyView = QtDeclarative.QDeclarativeView(SmileyWindow)
        self.smileyView.setObjectName(_fromUtf8("smileyView"))
        self.gridLayout.addWidget(self.smileyView, 0, 0, 1, 1)

        self.retranslateUi(SmileyWindow)
        QtCore.QMetaObject.connectSlotsByName(SmileyWindow)

    def retranslateUi(self, SmileyWindow):
        SmileyWindow.setWindowTitle(_translate("SmileyWindow", "Dialog", None))

from PyQt4 import QtDeclarative
