# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/NewpostWindow.ui'
#
# Created: Mon Oct  7 14:59:37 2013
#      by: PyQt4 UI code generator 4.9.1
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
        NewPostWindow.resize(562, 306)
        NewPostWindow.setAutoFillBackground(False)
        NewPostWindow.setProperty("unifiedTitleAndToolBarOnMac", False)
        self.verticalLayout_2 = QtGui.QVBoxLayout(NewPostWindow)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textEdit = WCompleteLineEdit(NewPostWindow)
        self.textEdit.setMouseTracking(True)
        self.textEdit.setFrameShadow(QtGui.QFrame.Sunken)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.label = QtGui.QLabel(NewPostWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Black"))
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(NewPostWindow)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.chk_comment = QtGui.QCheckBox(NewPostWindow)
        self.chk_comment.setObjectName(_fromUtf8("chk_comment"))
        self.horizontalLayout.addWidget(self.chk_comment)
        self.chk_repost = QtGui.QCheckBox(NewPostWindow)
        self.chk_repost.setObjectName(_fromUtf8("chk_repost"))
        self.horizontalLayout.addWidget(self.chk_repost)
        self.chk_comment_original = QtGui.QCheckBox(NewPostWindow)
        self.chk_comment_original.setObjectName(_fromUtf8("chk_comment_original"))
        self.horizontalLayout.addWidget(self.chk_comment_original)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.widget_2 = QtGui.QWidget(NewPostWindow)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        self.pushButton_picture = QtGui.QPushButton(self.widget_2)
        self.pushButton_picture.setObjectName(_fromUtf8("pushButton_picture"))
        self.gridLayout_2.addWidget(self.pushButton_picture, 0, 1, 1, 1)
        self.pushButton_cancel = QtGui.QPushButton(self.widget_2)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.gridLayout_2.addWidget(self.pushButton_cancel, 0, 3, 1, 1)
        self.pushButton_send = QtGui.QPushButton(self.widget_2)
        self.pushButton_send.setObjectName(_fromUtf8("pushButton_send"))
        self.gridLayout_2.addWidget(self.pushButton_send, 0, 4, 1, 1)
        self.pushButton = QtGui.QPushButton(self.widget_2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_2.addWidget(self.pushButton, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.widget_2)

        self.retranslateUi(NewPostWindow)
        QtCore.QObject.connect(self.pushButton_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), NewPostWindow.close)
        QtCore.QObject.connect(self.pushButton_picture, QtCore.SIGNAL(_fromUtf8("clicked()")), NewPostWindow.addImage)
        QtCore.QObject.connect(self.pushButton_send, QtCore.SIGNAL(_fromUtf8("clicked()")), NewPostWindow.send)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), NewPostWindow.showSmiley)
        QtCore.QObject.connect(self.textEdit, QtCore.SIGNAL(_fromUtf8("textChanged()")), NewPostWindow.checkChars)
        QtCore.QMetaObject.connectSlotsByName(NewPostWindow)

    def retranslateUi(self, NewPostWindow):
        NewPostWindow.setWindowTitle(QtGui.QApplication.translate("NewPostWindow", "New Message", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewPostWindow", "140", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewPostWindow", "Also:", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_comment.setText(QtGui.QApplication.translate("NewPostWindow", "Comment", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_repost.setText(QtGui.QApplication.translate("NewPostWindow", "Repost", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_comment_original.setText(QtGui.QApplication.translate("NewPostWindow", "Commmet to Original", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_picture.setText(QtGui.QApplication.translate("NewPostWindow", "&Picture", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_cancel.setText(QtGui.QApplication.translate("NewPostWindow", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_send.setText(QtGui.QApplication.translate("NewPostWindow", "&Send", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("NewPostWindow", "S&miley", None, QtGui.QApplication.UnicodeUTF8))

from WCompleteLineEdit import WCompleteLineEdit
