# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/NewpostWindow.ui'
#
# Created: Mon Feb 11 19:25:22 2013
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_NewPostWindow(object):
    def setupUi(self, NewPostWindow):
        NewPostWindow.setObjectName(_fromUtf8("NewPostWindow"))
        NewPostWindow.resize(562, 386)
        NewPostWindow.setAutoFillBackground(False)
        NewPostWindow.setProperty("unifiedTitleAndToolBarOnMac", False)
        self.gridLayout_3 = QtGui.QGridLayout(NewPostWindow)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(NewPostWindow)
        self.widget.setMinimumSize(QtCore.QSize(0, 200))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QtGui.QTextEdit(self.widget)
        self.textEdit.setMouseTracking(True)
        self.textEdit.setFrameShadow(QtGui.QFrame.Sunken)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.widget_2 = QtGui.QWidget(NewPostWindow)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButton_at = QtGui.QPushButton(self.widget_2)
        self.pushButton_at.setObjectName(_fromUtf8("pushButton_at"))
        self.gridLayout_2.addWidget(self.pushButton_at, 0, 0, 1, 1)
        self.pushButton_picture = QtGui.QPushButton(self.widget_2)
        self.pushButton_picture.setObjectName(_fromUtf8("pushButton_picture"))
        self.gridLayout_2.addWidget(self.pushButton_picture, 0, 1, 1, 1)
        self.pushButton_send = QtGui.QPushButton(self.widget_2)
        self.pushButton_send.setObjectName(_fromUtf8("pushButton_send"))
        self.gridLayout_2.addWidget(self.pushButton_send, 0, 5, 1, 1)
        self.pushButton_location = QtGui.QPushButton(self.widget_2)
        self.pushButton_location.setObjectName(_fromUtf8("pushButton_location"))
        self.gridLayout_2.addWidget(self.pushButton_location, 0, 2, 1, 1)
        self.pushButton_cancel = QtGui.QPushButton(self.widget_2)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.gridLayout_2.addWidget(self.pushButton_cancel, 0, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.widget_2)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(NewPostWindow)
        QtCore.QMetaObject.connectSlotsByName(NewPostWindow)

    def retranslateUi(self, NewPostWindow):
        NewPostWindow.setWindowTitle(_translate("NewPostWindow", "New Message", None))
        self.pushButton_at.setText(_translate("NewPostWindow", "At", None))
        self.pushButton_picture.setText(_translate("NewPostWindow", "Picture", None))
        self.pushButton_send.setText(_translate("NewPostWindow", "Send", None))
        self.pushButton_location.setText(_translate("NewPostWindow", "Location", None))
        self.pushButton_cancel.setText(_translate("NewPostWindow", "Cancel", None))

