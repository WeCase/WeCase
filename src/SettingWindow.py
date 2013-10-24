#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented SettingWindow.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui
from SettingWindow_ui import Ui_SettingWindow
import path
from WeHack import async, start, getDirSize, clearDir
from WeCaseConfig import WeCaseConfig


class WeSettingsWindow(QtGui.QDialog, Ui_SettingWindow):

    cacheCleared = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WeSettingsWindow, self).__init__(parent)
        self.setupUi(self)
        self.loadConfig()
        self.cacheCleared.connect(self.showSize)
        self.needRestart = False

    def setupUi(self, widget):
        super(WeSettingsWindow, self).setupUi(widget)
        self.showSize()

    def showSize(self):
        self.cacheSizeLabel.setText(self.getHumanReadableCacheSize())

    def getHumanReadableCacheSize(self):
        raw_bytes = getDirSize(path.cache_path)
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
        self.config = WeCaseConfig(path.config_path)

        self.intervalSlider.setValue(self.config.notify_interval)
        self.setIntervalText(self.intervalSlider.value())
        self.timeoutSlider.setValue(self.config.notify_timeout)
        self.setTimeoutText(self.timeoutSlider.value())
        self.commentsChk.setChecked(self.config.remind_comments)
        self.mentionsChk.setChecked(self.config.remind_mentions)
        self.usersBlackListWidget.addItems(self.config.usersBlacklist)
        self.tweetsKeywordsBlacklistWidget.addItems(self.config.tweetsKeywordsBlacklist)
        self.blockWordwarsCheckBox.setChecked(self.config.blockWordwars)
        self.maxRetweetsCheckBox.setChecked(self.config.maxRetweets != -1)
        self.maxRetweetsLimitLineEdit.setText("" if self.config.maxRetweets == -1 else str(self.config.maxRetweets))
        self.maxTweetsPerUserCheckBox.setChecked(self.config.maxTweetsPerUser != -1)
        self.maxTweetsPerUserLimitLineEdit.setText("" if self.config.maxTweetsPerUser == -1 else str(self.config.maxTweetsPerUser))

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
        self.config.blockWordwars = str(self.blockWordwarsCheckBox.isChecked())
        self.config.maxRetweets = str(-1 if not self.maxRetweetsCheckBox.isChecked() else int(self.maxRetweetsLimitLineEdit.text()))
        self.config.maxTweetsPerUser = str(-1 if not self.maxTweetsPerUserCheckBox.isChecked() else int(self.maxTweetsPerUserLimitLineEdit.text()))
        self.config.save()

    def addBlackUser(self):
        self.needRestart = True
        user = QtGui.QInputDialog.getText(
            self, self.tr("Input A user:"),
            self.tr("Please input a user"),
            QtGui.QLineEdit.Normal, self.tr("Username"))[0]
        if user:
            self.usersBlackListWidget.addItem(user)

    def removeBlackUser(self):
        self.needRestart = True
        row = self.usersBlackListWidget.currentRow()
        self.usersBlackListWidget.takeItem(row)

    def addKeyword(self):
        self.needRestart = True
        keyword = QtGui.QInputDialog.getText(
            self,
            self.tr("Input a keyword:"),
            self.tr("Please input a keyword"),
            QtGui.QLineEdit.Normal, self.tr("Keyword"))[0]
        if keyword:
            self.tweetsKeywordsBlacklistWidget.addItem(keyword)

    def removeKeyword(self):
        self.needRestart = True
        row = self.tweetsKeywordsBlacklistWidget.currentRow()
        self.tweetsKeywordsBlacklistWidget.takeItem(row)

    def accept(self):
        self.saveConfig()
        if self.needRestart:
            QtGui.QMessageBox.information(
                self, self.tr("Restart"),
                self.tr("Settings need to restart WeCase to take effect."))
        self.done(True)

    def reject(self):
        self.done(False)

    @async
    def clearCache(self):
        clearDir(path.cache_path)
        self.needRestart = True
        self.cacheCleared.emit()

    def viewCache(self):
        start(path.cache_path)
