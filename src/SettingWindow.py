#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented SettingWindow.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui
from SettingWindow_ui import Ui_SettingWindow
import const
from WeHack import async, start, getDirSize, clearDir
from WeCaseConfig import WeCaseConfig


class WeSettingsWindow(QtGui.QDialog, Ui_SettingWindow):

    cacheCleared = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WeSettingsWindow, self).__init__(parent)
        self.setupUi(self)
        self.loadConfig()
        self.cacheCleared.connect(self.showSize)

    def setupUi(self, widget):
        super(WeSettingsWindow, self).setupUi(widget)
        self.showSize()

    def showSize(self):
        self.cacheSizeLabel.setText(self.getHumanReadableCacheSize())

    def getHumanReadableCacheSize(self):
        raw_bytes = getDirSize(const.cache_path)
        megabytes_str = "%.1f MiB" % (raw_bytes / 1000000)
        return megabytes_str

    def transformInterval(self, sliderValue):
        return sliderValue // 60, sliderValue % 60

    def setIntervalText(self, sliderValue):
        self.intervalLabel.setText(self.tr("%i min %i sec") %
                                   (self.transformInterval(sliderValue)))

    def setTimeoutText(self, sliderValue):
        self.timeoutLabel.setText(self.tr("%i sec") % sliderValue)

    def loadConfig(self):
        self.config = WeCaseConfig(const.config_path)

        self.intervalSlider.setValue(self.config.notify_interval)
        self.setIntervalText(self.intervalSlider.value())
        self.timeoutSlider.setValue(self.config.notify_timeout)
        self.setTimeoutText(self.timeoutSlider.value())
        self.commentsChk.setChecked(self.config.remind_comments)
        self.mentionsChk.setChecked(self.config.remind_mentions)
        self.usersBlackListWidget.addItems(self.config.usersBlacklist)
        self.tweetsKeywordsBlacklistWidget.addItems(self.config.tweetsKeywordsBlacklist)

    def _getListWidgetItemsStringList(self, listWidget):
        stringList = []
        for i in range(0, listWidget.count()):
            stringList.append(listWidget.item(i).text())
        return stringList

    def saveConfig(self):
        self.config.notify_interval = str(self.intervalSlider.value())
        self.config.notify_timeout = str(self.timeoutSlider.value())
        self.config.remind_comments = str(self.commentsChk.isChecked())
        self.config.remind_mentions = str(self.mentionsChk.isChecked())
        self.config.usersBlacklist = str(self._getListWidgetItemsStringList(self.usersBlackListWidget))
        self.config.tweetsKeywordsBlacklist = str(self._getListWidgetItemsStringList(self.tweetsKeywordsBlacklistWidget))
        self.config.save()

    def addBlackUser(self):
        user = QtGui.QInputDialog.getText(
            self, self.tr("Input A user:"),
            self.tr("Please input a user"),
            QtGui.QLineEdit.Normal, self.tr("Username"))[0]
        if user:
            self.usersBlackListWidget.addItem(user)

    def removeBlackUser(self):
        row = self.usersBlackListWidget.currentRow()
        self.usersBlackListWidget.takeItem(row)

    def addKeyword(self):
        keyword = QtGui.QInputDialog.getText(
            self,
            self.tr("Input a keyword:"),
            self.tr("Please input a keyword"),
            QtGui.QLineEdit.Normal, self.tr("Keyword"))[0]
        if keyword:
            self.tweetsKeywordsBlacklistWidget.addItem(keyword)

    def removeKeyword(self):
        row = self.tweetsKeywordsBlacklistWidget.currentRow()
        self.tweetsKeywordsBlacklistWidget.takeItem(row)

    def accept(self):
        self.saveConfig()
        QtGui.QMessageBox.information(
            self, self.tr("Restart"),
            self.tr("Filter's settings need to restart WeCase to take effect."))
        self.done(True)

    def reject(self):
        self.done(False)

    @async
    def clearCache(self):
        clearDir(const.cache_path)
        self.cacheCleared.emit()

    def viewCache(self):
        start(const.cache_path)
