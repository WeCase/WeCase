# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/SettingWindow.ui'
#
# Created: Tue Feb 12 09:45:51 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SettingWindow(object):
    def setupUi(self, SettingWindow):
        SettingWindow.setObjectName(_fromUtf8("SettingWindow"))
        SettingWindow.resize(521, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/IMG/img/preferences-other.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SettingWindow.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(SettingWindow)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(SettingWindow)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.widget = QtGui.QWidget(SettingWindow)
        self.widget.setMinimumSize(QtCore.QSize(0, 30))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_OK = QtGui.QPushButton(self.widget)
        self.pushButton_OK.setObjectName(_fromUtf8("pushButton_OK"))
        self.gridLayout.addWidget(self.pushButton_OK, 0, 0, 1, 1)
        self.pushButton_Cancel = QtGui.QPushButton(self.widget)
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.gridLayout.addWidget(self.pushButton_Cancel, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(SettingWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingWindow)

    def retranslateUi(self, SettingWindow):
        SettingWindow.setWindowTitle(QtGui.QApplication.translate("SettingWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("SettingWindow", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("SettingWindow", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OK.setText(QtGui.QApplication.translate("SettingWindow", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("SettingWindow", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))

import wecase_rc
