# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Sun Feb 10 10:24:37 2013
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

class Ui_frm_MainWindow(object):
    def setupUi(self, frm_MainWindow):
        frm_MainWindow.setObjectName(_fromUtf8("frm_MainWindow"))
        frm_MainWindow.resize(404, 669)
        self.centralwidget = QtGui.QWidget(frm_MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(25)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setSizeIncrement(QtCore.QSize(0, 25))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabWidgetPage1 = QtGui.QWidget()
        self.tabWidgetPage1.setObjectName(_fromUtf8("tabWidgetPage1"))
        self.tabWidget.addTab(self.tabWidgetPage1, _fromUtf8(""))
        self.tabWidgetPage2 = QtGui.QWidget()
        self.tabWidgetPage2.setObjectName(_fromUtf8("tabWidgetPage2"))
        self.tabWidget.addTab(self.tabWidgetPage2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 30))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_3 = QtGui.QPushButton(self.widget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.widget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_4 = QtGui.QPushButton(self.widget)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout.addWidget(self.pushButton_4, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        frm_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(frm_MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 404, 26))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setMinimumSize(QtCore.QSize(0, 25))
        self.menubar.setDefaultUp(True)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_WeCase = QtGui.QMenu(self.menubar)
        self.menu_WeCase.setObjectName(_fromUtf8("menu_WeCase"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuO_ptions = QtGui.QMenu(self.menubar)
        self.menuO_ptions.setObjectName(_fromUtf8("menuO_ptions"))
        frm_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(frm_MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frm_MainWindow.setStatusBar(self.statusbar)
        self.action_About = QtGui.QAction(frm_MainWindow)
        self.action_About.setObjectName(_fromUtf8("action_About"))
        self.action_Refresh = QtGui.QAction(frm_MainWindow)
        self.action_Refresh.setObjectName(_fromUtf8("action_Refresh"))
        self.action_Log_out = QtGui.QAction(frm_MainWindow)
        self.action_Log_out.setObjectName(_fromUtf8("action_Log_out"))
        self.action_Exit = QtGui.QAction(frm_MainWindow)
        self.action_Exit.setObjectName(_fromUtf8("action_Exit"))
        self.action_Settings = QtGui.QAction(frm_MainWindow)
        self.action_Settings.setObjectName(_fromUtf8("action_Settings"))
        self.actionUpdate = QtGui.QAction(frm_MainWindow)
        self.actionUpdate.setObjectName(_fromUtf8("actionUpdate"))
        self.menu_WeCase.addAction(self.action_Refresh)
        self.menu_WeCase.addSeparator()
        self.menu_WeCase.addAction(self.action_Log_out)
        self.menu_WeCase.addAction(self.action_Exit)
        self.menuHelp.addAction(self.action_About)
        self.menuO_ptions.addAction(self.action_Settings)
        self.menuO_ptions.addAction(self.actionUpdate)
        self.menubar.addAction(self.menu_WeCase.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuO_ptions.menuAction())

        self.retranslateUi(frm_MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(frm_MainWindow)

    def retranslateUi(self, frm_MainWindow):
        frm_MainWindow.setWindowTitle(_translate("frm_MainWindow", "WeCase", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), _translate("frm_MainWindow", "微博", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), _translate("frm_MainWindow", "私信", None))
        self.pushButton_3.setText(_translate("frm_MainWindow", "Me", None))
        self.pushButton.setText(_translate("frm_MainWindow", "Refresh", None))
        self.pushButton_2.setText(_translate("frm_MainWindow", "New Weibo", None))
        self.pushButton_4.setText(_translate("frm_MainWindow", "Settings", None))
        self.menu_WeCase.setTitle(_translate("frm_MainWindow", "&WeCase", None))
        self.menuHelp.setTitle(_translate("frm_MainWindow", "&Help", None))
        self.menuO_ptions.setTitle(_translate("frm_MainWindow", "&Options", None))
        self.action_About.setText(_translate("frm_MainWindow", "&About...", None))
        self.action_Refresh.setText(_translate("frm_MainWindow", "&Refresh", None))
        self.action_Log_out.setText(_translate("frm_MainWindow", "&Log out", None))
        self.action_Exit.setText(_translate("frm_MainWindow", "&Exit", None))
        self.action_Settings.setText(_translate("frm_MainWindow", "&Settings", None))
        self.actionUpdate.setText(_translate("frm_MainWindow", "&Update", None))

