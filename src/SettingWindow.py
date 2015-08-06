# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented SettingWindow.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui
from SettingWindow_ui import Ui_SettingWindow
from FilterTable import FilterTableModel
import path
from WConfigParser import WConfigParser
from WeHack import async, start, getDirSize, clearDir


class WeSettingsWindow(QtGui.QDialog, Ui_SettingWindow):

    cacheCleared = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WeSettingsWindow, self).__init__(parent)
        self.setupUi(self)
        self.setupModel()
        self.setupSignal()
        self.loadConfig()
        self.cacheCleared.connect(self.showSize)
        self.needRestart = False

    def setupUi(self, widget):
        super(WeSettingsWindow, self).setupUi(widget)
        self.filterTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.showSize()

    def setupModel(self):
        self.filterModel = FilterTableModel(self.filterTable)
        self.filterTable.setModel(self.filterModel)

    def setupSignal(self):
        self.addRuleButton.clicked.connect(self.addRule)
        self.removeRuleButton.clicked.connect(self.removeRule)

    @QtCore.pyqtSlot()
    def addRule(self):
        self.needRestart = True
        self.filterModel.insertRows(self.filterModel.rowCount(), 1)

    @QtCore.pyqtSlot()
    def removeRule(self):
        self.needRestart = True
        row = self.filterTable.currentIndex().row()
        if row >= 0:
            self.filterModel.removeRows(row, 1)

    @QtCore.pyqtSlot()
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
        self.config = WConfigParser(path.myself_path + "WMetaConfig",
                                    path.config_path, "main")

        self.intervalSlider.setValue(self.config.notify_interval)
        self.setIntervalText(self.intervalSlider.value())
        self.timeoutSlider.setValue(self.config.notify_timeout)
        self.setTimeoutText(self.timeoutSlider.value())
        self.commentsChk.setChecked(self.config.remind_comments)
        self.mentionsChk.setChecked(self.config.remind_mentions)
        self.filterModel.loadKeywordsBlacklist(self.config.tweetsKeywordsBlacklist)
        self.filterModel.loadUsersBlacklist(self.config.usersBlacklist)
        self.filterModel.loadWordWarKeywords(self.config.wordWarKeywords)
        self.blockWordwarsCheckBox.setChecked(self.config.blockWordwars)
        self.maxRetweetsCheckBox.setChecked(self.config.maxRetweets != -1)
        self.maxRetweetsLimitLineEdit.setText("" if self.config.maxRetweets == -1 else str(self.config.maxRetweets))
        self.maxTweetsPerUserCheckBox.setChecked(self.config.maxTweetsPerUser != -1)
        self.maxTweetsPerUserLimitLineEdit.setText("" if self.config.maxTweetsPerUser == -1 else str(self.config.maxTweetsPerUser))
        self.regexCheckbox.setChecked(self.config.keywordsAsRegex)

    def saveConfig(self):
        self.config.notify_interval = str(self.intervalSlider.value())
        self.config.notify_timeout = str(self.timeoutSlider.value())
        self.config.remind_comments = str(self.commentsChk.isChecked())
        self.config.remind_mentions = str(self.mentionsChk.isChecked())
        self.config.tweetsKeywordsBlacklist = self.filterModel.dumpKeywordsBlacklist()
        self.config.usersBlacklist = self.filterModel.dumpUsersBlacklist()
        self.config.wordWarKeywords = self.filterModel.dumpWordWarKeywords()
        self.config.blockWordwars = str(self.blockWordwarsCheckBox.isChecked())
        self.config.maxRetweets = str(-1 if not self.maxRetweetsCheckBox.isChecked() else int(self.maxRetweetsLimitLineEdit.text()))
        self.config.maxTweetsPerUser = str(-1 if not self.maxTweetsPerUserCheckBox.isChecked() else int(self.maxTweetsPerUserLimitLineEdit.text()))
        self.config.keywordsAsRegex = str(self.regexCheckbox.isChecked())
        self.config.save()

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
