# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/LoginWindow.ui'
#
# Created: Sun Mar 31 14:15:14 2013
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

class Ui_frm_Login(object):
    def setupUi(self, frm_Login):
        frm_Login.setObjectName(_fromUtf8("frm_Login"))
        frm_Login.setWindowModality(QtCore.Qt.WindowModal)
        frm_Login.resize(312, 133)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frm_Login.sizePolicy().hasHeightForWidth())
        frm_Login.setSizePolicy(sizePolicy)
        frm_Login.setMinimumSize(QtCore.QSize(312, 133))
        frm_Login.setMaximumSize(QtCore.QSize(312, 133))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/IMG/img/WeCase.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frm_Login.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(frm_Login)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_username = QtGui.QLabel(frm_Login)
        self.label_username.setObjectName(_fromUtf8("label_username"))
        self.verticalLayout_2.addWidget(self.label_username)
        self.label_passwd = QtGui.QLabel(frm_Login)
        self.label_passwd.setObjectName(_fromUtf8("label_passwd"))
        self.verticalLayout_2.addWidget(self.label_passwd)
        self.label_status = QtGui.QLabel(frm_Login)
        self.label_status.setObjectName(_fromUtf8("label_status"))
        self.verticalLayout_2.addWidget(self.label_status)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cmb_Users = QtGui.QComboBox(frm_Login)
        self.cmb_Users.setEditable(True)
        self.cmb_Users.setObjectName(_fromUtf8("cmb_Users"))
        self.verticalLayout.addWidget(self.cmb_Users)
        self.txt_Password = QtGui.QLineEdit(frm_Login)
        self.txt_Password.setObjectName(_fromUtf8("txt_Password"))
        self.verticalLayout.addWidget(self.txt_Password)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.chk_Remember = QtGui.QCheckBox(frm_Login)
        self.chk_Remember.setObjectName(_fromUtf8("chk_Remember"))
        self.horizontalLayout_2.addWidget(self.chk_Remember)
        self.chk_AutoLogin = QtGui.QCheckBox(frm_Login)
        self.chk_AutoLogin.setObjectName(_fromUtf8("chk_AutoLogin"))
        self.horizontalLayout_2.addWidget(self.chk_AutoLogin)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_log = QtGui.QPushButton(frm_Login)
        self.pushButton_log.setDefault(True)
        self.pushButton_log.setObjectName(_fromUtf8("pushButton_log"))
        self.horizontalLayout.addWidget(self.pushButton_log)
        self.pushButton_new = QtGui.QPushButton(frm_Login)
        self.pushButton_new.setObjectName(_fromUtf8("pushButton_new"))
        self.horizontalLayout.addWidget(self.pushButton_new)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.label_username.setBuddy(self.cmb_Users)
        self.label_passwd.setBuddy(self.txt_Password)

        self.retranslateUi(frm_Login)
        QtCore.QObject.connect(self.cmb_Users, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), frm_Login.setPassword)
        QtCore.QObject.connect(self.chk_AutoLogin, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.chk_Remember.setChecked)
        QtCore.QObject.connect(self.pushButton_log, QtCore.SIGNAL(_fromUtf8("clicked()")), frm_Login.login)
        QtCore.QObject.connect(self.pushButton_new, QtCore.SIGNAL(_fromUtf8("clicked()")), frm_Login.openRegisterPage)
        QtCore.QMetaObject.connectSlotsByName(frm_Login)
        frm_Login.setTabOrder(self.pushButton_log, self.cmb_Users)
        frm_Login.setTabOrder(self.cmb_Users, self.txt_Password)
        frm_Login.setTabOrder(self.txt_Password, self.chk_Remember)
        frm_Login.setTabOrder(self.chk_Remember, self.chk_AutoLogin)
        frm_Login.setTabOrder(self.chk_AutoLogin, self.pushButton_new)

    def retranslateUi(self, frm_Login):
        frm_Login.setWindowTitle(_translate("frm_Login", "Log in", None))
        self.label_username.setText(_translate("frm_Login", "User Name:", None))
        self.label_passwd.setText(_translate("frm_Login", "Password:", None))
        self.label_status.setText(_translate("frm_Login", "Status:", None))
        self.chk_Remember.setText(_translate("frm_Login", "Remember Me", None))
        self.chk_AutoLogin.setText(_translate("frm_Login", "Auto Login", None))
        self.pushButton_log.setText(_translate("frm_Login", "GO!", None))
        self.pushButton_new.setText(_translate("frm_Login", "New account", None))

import wecase_rc
