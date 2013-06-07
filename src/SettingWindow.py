#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented SettingWindow.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


from PyQt4 import QtGui
from configparser import ConfigParser
from SettingWindow_ui import Ui_SettingWindow
import const


class WeSettingsWindow(QtGui.QDialog, Ui_SettingWindow):
    def __init__(self, parent=None):
        super(WeSettingsWindow, self).__init__(parent)
        self.setupUi(self)
        self.loadConfig()

    def transformInterval(self, sliderValue):
        return (sliderValue // 60, sliderValue % 60)

    def setIntervalText(self, sliderValue):
        self.intervalLabel.setText(self.tr("%i min %i sec") %
                                   (self.transformInterval(sliderValue)))

    def setTimeoutText(self, sliderValue):
        self.timeoutLabel.setText(self.tr("%i sec") % sliderValue)

    def loadConfig(self):
        self.config = ConfigParser()
        self.config.read(const.config_path)

        if not self.config.has_section('main'):
            self.config['main'] = {}

        self.main_config = self.config['main']
        self.intervalSlider.setValue(int(self.main_config.get(
            'notify_interval', "30")))
        self.setIntervalText(self.intervalSlider.value())
        self.timeoutSlider.setValue(int(self.main_config.get(
            "notify_timeout", "5")))
        self.setTimeoutText(self.timeoutSlider.value())
        self.commentsChk.setChecked(self.main_config.getboolean(
            "remind_comments", True))
        self.mentionsChk.setChecked(self.main_config.getboolean(
            "remind_mentions", True))
        self.usersBlackListWidget.addItems(eval(self.main_config.get(
            "usersBlacklist", "[]")))
        self.tweetsKeywordsBlacklistWidget.addItems(eval(self.main_config.get(
            "tweetKeywordsBlacklist", "[]")))

    def _getListWidgetItemsStringList(self, listWidget):
        stringList = []
        for i in range(0, listWidget.count()):
            stringList.append(listWidget.item(i).text())
        return stringList

    def saveConfig(self):
        self.config = ConfigParser()
        self.config.read(const.config_path)

        if not self.config.has_section('main'):
            self.config['main'] = {}

        self.main_config = self.config['main']
        self.main_config['notify_interval'] = str(self.intervalSlider.value())
        self.main_config['notify_timeout'] = str(self.timeoutSlider.value())
        self.main_config['remind_comments'] = str(self.commentsChk.isChecked())
        self.main_config['remind_mentions'] = str(self.mentionsChk.isChecked())
        self.main_config['usersBlacklist'] = str(self._getListWidgetItemsStringList(self.usersBlackListWidget))
        self.main_config['tweetKeywordsBlacklist'] = str(self._getListWidgetItemsStringList(self.tweetsKeywordsBlacklistWidget))

        with open(const.config_path, "w+") as config_file:
            self.config.write(config_file)

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
