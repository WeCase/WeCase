#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented WeCaseWindow, the mainWindow of WeCase.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import os
import urllib.request
import urllib.parse
import urllib.error
from configparser import ConfigParser
import threading
from WTimer import WTimer
from PyQt4 import QtCore, QtGui
from Tweet import TweetCommonModel, TweetCommentModel, TweetItem
from MainWindow_ui import Ui_frm_MainWindow
from Notify import Notify
from NewpostWindow import NewpostWindow
from SettingWindow import WeSettingsWindow
from AboutWindow import AboutWindow
import const


class WeCaseWindow(QtGui.QMainWindow, Ui_frm_MainWindow):
    client = None
    uid = None
    imageLoaded = QtCore.pyqtSignal(str)
    tabTextChanged = QtCore.pyqtSignal(int, str)

    def __init__(self, client, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.tweetViews = [self.homeView, self.mentionsView, self.commentsView,
                           self.myView]
        self.scrollAreas = [self.scrollArea, self.scrollArea_2, self.scrollArea_3,
                            self.scrollArea_4]
        self.client = client
        self.setupModels()
        self.init_account()
        self.setupMyUi()
        self.loadConfig()
        self.IMG_AVATAR = -2
        self.IMG_THUMB = -1
        self.notify = Notify(timeout=self.notify_timeout)
        self.applyConfig()
        self.download_lock = []

    def init_account(self):
        self.get_uid()

    def loadConfig(self):
        self.config = ConfigParser()
        self.config.read(const.config_path)

        if not self.config.has_section('main'):
            self.config['main'] = {}

        self.main_config = self.config['main']
        self.timer_interval = int(self.main_config.get('notify_interval', 30))
        self.notify_timeout = int(self.main_config.get('notify_timeout', 5))
        self.remindMentions = self.main_config.getboolean('remind_mentions', 1)
        self.remindComments = self.main_config.getboolean('remind_comments', 1)

    def applyConfig(self):
        try:
            self.timer.stop_event.set()
        except AttributeError:
            pass

        self.timer = WTimer(self.timer_interval, self.show_notify)
        self.timer.start()
        self.notify.timeout = self.notify_timeout

    def setupMyUi(self):
        return

    def load_more(self, value):
        if value == self.get_current_scrollArea().verticalScrollBar().maximum():
            model = self.get_current_model()
            model.next()

    def setupModels(self):
        for view in self.tweetViews:
            view.client = self.client

        for scrollArea in self.scrollAreas:
            scrollArea.verticalScrollBar().valueChanged.connect(self.load_more)

        self.all_timeline = TweetCommonModel(
                                             self.client.statuses.home_timeline,
                                             self)
        self.all_timeline.load()
        self.homeView.setModel(self.all_timeline)
        self.homeView.clicked.connect(self.test)

        self.mentions = TweetCommonModel(
                                         self.client.statuses.mentions,
                                         self)
        self.mentions.load()
        self.mentionsView.setModel(self.mentions)

        self.comment_to_me = TweetCommentModel(
                                               self.client.comments.to_me,
                                               self)
        self.comment_to_me.load()
        self.commentsView.setModel(self.comment_to_me)

        self.my_timeline = TweetCommonModel(
                                            self.client.statuses.user_timeline,
                                            self)
        self.my_timeline.load()
        self.myView.setModel(self.my_timeline)

    def test(self):
        print("Test")

    def reset_remind(self):
        if self.tabWidget.currentIndex() == 0:
            self.tabWidget.setTabText(0, self.tr("Weibo"))
        elif self.tabWidget.currentIndex() == 1:
            self.client.remind.set_count.post(type="mention_status")
            self.tabWidget.setTabText(1, self.tr("@Me"))
        elif self.tabWidget.currentIndex() == 2:
            self.client.remind.set_count.post(type="cmt")
            self.tabWidget.setTabText(2, self.tr("Comments"))

    def get_remind(self, uid):
        '''this function is used to get unread_count
        from Weibo API. uid is necessary.'''

        reminds = self.client.remind.unread_count.get(uid=uid)
        return reminds

    def get_uid(self):
        '''How can I get my uid? here it is'''
        try:
            self.uid = self.client.account.get_uid.get().uid
        except AttributeError:
            return None

    def show_notify(self):
        # This function is run in another thread by WTimer.
        # Do not modify UI directly. Send signal and react it in a slot only.
        # We use SIGNAL self.tabTextChanged and SLOT self.setTabText()
        # to display unread count

        reminds = self.get_remind(self.uid)
        msg = self.tr("You have:") + "\n"
        num_msg = 0

        if reminds['status'] != 0:
            # Note: do NOT send notify here, or users will crazy.
            self.tabTextChanged.emit(0, self.tr("Weibo(%d)")
                                     % reminds['status'])

        if reminds['mention_status'] and self.remindMentions:
            msg += self.tr("%d unread @ME") % reminds['mention_status'] + "\n"
            self.tabTextChanged.emit(1, self.tr("@Me(%d)")
                                     % reminds['mention_status'])
            num_msg += 1

        if reminds['cmt'] and self.remindComments:
            msg += self.tr("%d unread comment(s)") % reminds['cmt'] + "\n"
            self.tabTextChanged.emit(2, self.tr("Comments(%d)")
                                     % reminds['cmt'])
            num_msg += 1

        if num_msg:
            return
            self.notify.showMessage(self.tr("WeCase"), msg)

    def setTabText(self, index, string):
        self.tabWidget.setTabText(index, string)

    def moveToTop(self):
        self.get_current_scrollArea().verticalScrollBar().setSliderPosition(0)

    def setLoaded(self, tweetid):
        pass
        #self.get_current_tweetView().rootObject().imageLoaded(tweetid)

    def showSettings(self):
        wecase_settings = WeSettingsWindow()
        if wecase_settings.exec_():
            self.loadConfig()
            self.applyConfig()

    def showAbout(self):
        wecase_about = AboutWindow()
        wecase_about.exec_()

    def logout(self):
        self.close()
        # This is a model dialog, if we exec it before we close MainWindow
        # MainWindow won't close
        from LoginWindow import LoginWindow
        wecase_login = LoginWindow()
        wecase_login.exec_()

    def postTweet(self):
        wecase_new = NewpostWindow(self.client)
        wecase_new.exec_()

    def refresh(self):
        model = self.get_current_model()
        model.timelineLoaded.connect(self.moveToTop)
        #model.clear()
        #model.load()
        model.new()
        self.reset_remind()

    def get_current_tweetView(self):
        tweetViews = {0: self.homeView, 1: self.mentionsView,
                      2: self.commentsView, 3: self.myView}
        return tweetViews[self.tabWidget.currentIndex()]

    def get_current_scrollArea(self):
        tweetViews = {0: self.scrollArea, 1: self.scrollArea_2,
                      2: self.scrollArea_3, 3: self.scrollArea_4}
        return tweetViews[self.tabWidget.currentIndex()]

    def get_current_model(self):
        models = {0: self.all_timeline, 1: self.mentions,
                  2: self.comment_to_me,
                  3: self.my_timeline}
        return models[self.tabWidget.currentIndex()]

    def get_current_function(self):
        functions = {0: self.get_all_timeline, 1: self.get_mentions_timeline,
                     2: self.get_comment_to_me, 3: self.get_my_timeline}
        return functions[self.tabWidget.currentIndex()]

    def closeEvent(self, event):
        self.timer.stop_event.set()
