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

        with open(const.config_path, "w+") as config_file:
            self.config.write(config_file)

    def accept(self):
        self.saveConfig()
        self.done(True)

    def reject(self):
        self.done(False)
