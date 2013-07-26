# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/FaceWindow.ui'
#
# Created: Fri Jul 26 18:36:55 2013
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_FaceWindow(object):
    def setupUi(self, FaceWindow):
        FaceWindow.setObjectName(_fromUtf8("FaceWindow"))
        FaceWindow.resize(533, 288)
        self.gridLayout = QtGui.QGridLayout(FaceWindow)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.faceView = WFaceListWidget(FaceWindow)
        self.faceView.setObjectName(_fromUtf8("faceView"))
        self.gridLayout.addWidget(self.faceView, 0, 0, 1, 1)

        self.retranslateUi(FaceWindow)
        QtCore.QMetaObject.connectSlotsByName(FaceWindow)

    def retranslateUi(self, FaceWindow):
        FaceWindow.setWindowTitle(_translate("FaceWindow", "Choose a smiley", None))

from FaceWidget import WFaceListWidget
