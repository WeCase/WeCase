# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewpostWindow.ui'
#
# Created: Fri Feb 15 18:34:30 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
        self.label = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Black"))
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.widget_2 = QtGui.QWidget(NewPostWindow)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButton_location = QtGui.QPushButton(self.widget_2)
        self.pushButton_location.setObjectName(_fromUtf8("pushButton_location"))
        self.gridLayout_2.addWidget(self.pushButton_location, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 3, 1, 1)
        self.pushButton_cancel = QtGui.QPushButton(self.widget_2)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.gridLayout_2.addWidget(self.pushButton_cancel, 0, 4, 1, 1)
        self.pushButton_picture = QtGui.QPushButton(self.widget_2)
        self.pushButton_picture.setObjectName(_fromUtf8("pushButton_picture"))
        self.gridLayout_2.addWidget(self.pushButton_picture, 0, 1, 1, 1)
        self.pushButton_at = QtGui.QPushButton(self.widget_2)
        self.pushButton_at.setObjectName(_fromUtf8("pushButton_at"))
        self.gridLayout_2.addWidget(self.pushButton_at, 0, 0, 1, 1)
        self.pushButton_send = QtGui.QPushButton(self.widget_2)
        self.pushButton_send.setObjectName(_fromUtf8("pushButton_send"))
        self.gridLayout_2.addWidget(self.pushButton_send, 0, 5, 1, 1)
        self.verticalLayout.addWidget(self.widget_2)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(NewPostWindow)
        QtCore.QObject.connect(self.pushButton_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), NewPostWindow.close)
        QtCore.QMetaObject.connectSlotsByName(NewPostWindow)

    def retranslateUi(self, NewPostWindow):
        NewPostWindow.setWindowTitle(QtGui.QApplication.translate("NewPostWindow", "New Message", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewPostWindow", "140", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_location.setText(QtGui.QApplication.translate("NewPostWindow", "Location", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_cancel.setText(QtGui.QApplication.translate("NewPostWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_picture.setText(QtGui.QApplication.translate("NewPostWindow", "Picture", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_at.setText(QtGui.QApplication.translate("NewPostWindow", "At", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_send.setText(QtGui.QApplication.translate("NewPostWindow", "Send", None, QtGui.QApplication.UnicodeUTF8))

