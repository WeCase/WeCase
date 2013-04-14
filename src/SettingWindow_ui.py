# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/SettingWindow.ui'
#
# Created: Sun Apr 14 21:55:20 2013
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

class Ui_SettingWindow(object):
    def setupUi(self, SettingWindow):
        SettingWindow.setObjectName(_fromUtf8("SettingWindow"))
        SettingWindow.resize(360, 187)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingWindow.sizePolicy().hasHeightForWidth())
        SettingWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/IMG/img/preferences-other.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SettingWindow.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(SettingWindow)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(SettingWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.intervalDefine = QtGui.QLabel(self.tab)
        self.intervalDefine.setObjectName(_fromUtf8("intervalDefine"))
        self.horizontalLayout_2.addWidget(self.intervalDefine)
        self.intervalSlider = QtGui.QSlider(self.tab)
        self.intervalSlider.setMinimum(5)
        self.intervalSlider.setMaximum(360)
        self.intervalSlider.setSingleStep(30)
        self.intervalSlider.setPageStep(0)
        self.intervalSlider.setProperty("value", 5)
        self.intervalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.intervalSlider.setObjectName(_fromUtf8("intervalSlider"))
        self.horizontalLayout_2.addWidget(self.intervalSlider)
        self.intervalLabel = QtGui.QLabel(self.tab)
        self.intervalLabel.setObjectName(_fromUtf8("intervalLabel"))
        self.horizontalLayout_2.addWidget(self.intervalLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.timeoutDefine = QtGui.QLabel(self.tab)
        self.timeoutDefine.setObjectName(_fromUtf8("timeoutDefine"))
        self.horizontalLayout_4.addWidget(self.timeoutDefine)
        self.timeoutSlider = QtGui.QSlider(self.tab)
        self.timeoutSlider.setMinimum(1)
        self.timeoutSlider.setMaximum(100)
        self.timeoutSlider.setSingleStep(30)
        self.timeoutSlider.setPageStep(0)
        self.timeoutSlider.setProperty("value", 1)
        self.timeoutSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeoutSlider.setObjectName(_fromUtf8("timeoutSlider"))
        self.horizontalLayout_4.addWidget(self.timeoutSlider)
        self.timeoutLabel = QtGui.QLabel(self.tab)
        self.timeoutLabel.setObjectName(_fromUtf8("timeoutLabel"))
        self.horizontalLayout_4.addWidget(self.timeoutLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mentionsChk = QtGui.QCheckBox(self.tab)
        self.mentionsChk.setObjectName(_fromUtf8("mentionsChk"))
        self.horizontalLayout.addWidget(self.mentionsChk)
        self.commentsChk = QtGui.QCheckBox(self.tab)
        self.commentsChk.setObjectName(_fromUtf8("commentsChk"))
        self.horizontalLayout.addWidget(self.commentsChk)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(SettingWindow)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout.setStretch(0, 6)
        self.intervalDefine.setBuddy(self.intervalSlider)
        self.timeoutDefine.setBuddy(self.intervalSlider)
        self.label_2.setBuddy(self.mentionsChk)

        self.retranslateUi(SettingWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.intervalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), SettingWindow.setIntervalText)
        QtCore.QObject.connect(self.timeoutSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), SettingWindow.setTimeoutText)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SettingWindow.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SettingWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingWindow)

    def retranslateUi(self, SettingWindow):
        SettingWindow.setWindowTitle(_translate("SettingWindow", "Settings", None))
        self.intervalDefine.setText(_translate("SettingWindow", "Interval for notify checking", None))
        self.intervalLabel.setText(_translate("SettingWindow", "? ms", None))
        self.timeoutDefine.setText(_translate("SettingWindow", "Timeout for popup notify", None))
        self.timeoutLabel.setText(_translate("SettingWindow", "? ms", None))
        self.label_2.setText(_translate("SettingWindow", "Remind me when I have:", None))
        self.mentionsChk.setText(_translate("SettingWindow", "@ Me", None))
        self.commentsChk.setText(_translate("SettingWindow", "Comments", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("SettingWindow", "Notify", None))

import wecase_rc
