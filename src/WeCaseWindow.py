#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented WeCaseWindow, the mainWindow of WeCase.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import http
from time import sleep
from WTimer import WTimer
from PyQt4 import QtCore, QtGui
from Tweet import TweetCommonModel, TweetCommentModel
from MainWindow_ui import Ui_frm_MainWindow
from Notify import Notify
from NewpostWindow import NewpostWindow
from SettingWindow import WeSettingsWindow
from AboutWindow import AboutWindow
import const
from WeCaseConfig import WeCaseConfig
from WeHack import async
from WeRuntimeInfo import WeRuntimeInfo


class WeCaseWindow(QtGui.QMainWindow, Ui_frm_MainWindow):
    client = None
    uid = None
    imageLoaded = QtCore.pyqtSignal(str)
    tabTextChanged = QtCore.pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(WeCaseWindow, self).__init__(parent)
        self.setupUi(self)
        self.tweetViews = [self.homeView, self.mentionsView,
                           self.commentsView, self.myView]
        self.info = WeRuntimeInfo()
        self.client = const.client
        self.loadConfig()
        self.init_account()
        self.setupModels()
        self.IMG_AVATAR = -2
        self.IMG_THUMB = -1
        self.notify = Notify(timeout=self.notify_timeout)
        self.applyConfig()
        self.download_lock = []

    def setupUi(self, widget):
        super(WeCaseWindow, self).setupUi(widget)
        self.action_Refresh.setShortcut(QtGui.QKeySequence("F5"))
        self._setTabIcon(0, QtGui.QPixmap(const.icon("sina.png")))
        self._setTabIcon(1, QtGui.QPixmap(const.icon("mentions.png")))
        self._setTabIcon(2, QtGui.QPixmap(const.icon("comments2.png")))

    def _setTabIcon(self, index, icon):
        icon = QtGui.QIcon(icon.transformed(QtGui.QTransform().rotate(90)))
        self.tabWidget.setTabIcon(index, icon)
        self.tabWidget.setIconSize(QtCore.QSize(24, 24))

    def init_account(self):
        self.uid()

    def loadConfig(self):
        self.config = WeCaseConfig(const.config_path)
        self.notify_interval = self.config.notify_interval
        self.notify_timeout = self.config.notify_timeout
        self.usersBlacklist = self.config.usersBlacklist
        self.tweetKeywordsBlacklist = self.config.tweetsKeywordsBlacklist
        self.remindMentions = self.config.remind_mentions
        self.remindComments = self.config.remind_comments

    def applyConfig(self):
        try:
            self.timer.stop_event.set()
        except AttributeError:
            pass

        self.timer = WTimer(self.notify_interval, self.show_notify)
        self.timer.start()
        self.notify.timeout = self.notify_timeout

    def setupModels(self):
        self.all_timeline = TweetCommonModel(self.client.statuses.home_timeline, self)
        self.all_timeline.setUsersBlacklist(self.usersBlacklist)
        self.all_timeline.setTweetsKeywordsBlacklist(self.tweetKeywordsBlacklist)
        self.all_timeline.load()
        self.homeView.setModel(self.all_timeline)

        self.mentions = TweetCommonModel(self.client.statuses.mentions, self)
        self.mentions.setUsersBlacklist(self.usersBlacklist)
        self.mentions.setTweetsKeywordsBlacklist(self.tweetKeywordsBlacklist)
        self.mentions.load()
        self.mentionsView.setModel(self.mentions)

        self.comment_to_me = TweetCommentModel(self.client.comments.to_me, self)
        self.comment_to_me.setUsersBlacklist(self.usersBlacklist)
        self.comment_to_me.setTweetsKeywordsBlacklist(self.tweetKeywordsBlacklist)
        self.comment_to_me.load()
        self.commentsView.setModel(self.comment_to_me)

        self.my_timeline = TweetCommonModel(self.client.statuses.user_timeline, self)
        self.my_timeline.setUsersBlacklist(self.usersBlacklist)
        self.my_timeline.setTweetsKeywordsBlacklist(self.tweetKeywordsBlacklist)
        self.my_timeline.load()
        self.myView.setModel(self.my_timeline)

    @async
    def reset_remind(self):
        if self.currentTweetView() == self.homeView:
            self.tabTextChanged.emit(self.tabWidget.currentIndex(),
                                     self.tr("Weibo"))
        elif self.currentTweetView() == self.mentionsView:
            self.client.remind.set_count.post(type="mention_status")
            self.tabTextChanged.emit(self.tabWidget.currentIndex(),
                                     self.tr("@Me"))
        elif self.currentTweetView() == self.commentsView:
            self.client.remind.set_count.post(type="cmt")
            self.tabTextChanged.emit(self.tabWidget.currentIndex(),
                                     self.tr("Comments"))

    def get_remind(self, uid):
        """this function is used to get unread_count
        from Weibo API. uid is necessary."""

        while 1:
            try:
                reminds = self.client.remind.unread_count.get(uid=uid)
                break
            except http.client.BadStatusLine:
                sleep(0.2)
                continue
        return reminds

    def uid(self):
        """How can I get my uid? here it is"""
        if not self.info.get("uid"):
            self.info["uid"] = self.client.account.get_uid.get().uid
        return self.info["uid"]

    def show_notify(self):
        # This function is run in another thread by WTimer.
        # Do not modify UI directly. Send signal and react it in a slot only.
        # We use SIGNAL self.tabTextChanged and SLOT self.setTabText()
        # to display unread count

        reminds = self.get_remind(self.uid())
        msg = self.tr("You have:") + "\n"
        num_msg = 0

        if reminds['status'] != 0:
            # Note: do NOT send notify here, or users will crazy.
            print("Got it!")
            self.tabTextChanged.emit(self.tabWidget.indexOf(self.homeTab),
                                     self.tr("Weibo(%d)")
                                     % reminds['status'])

        if reminds['mention_status'] and self.remindMentions:
            msg += self.tr("%d unread @ME") % reminds['mention_status'] + "\n"
            self.tabTextChanged.emit(self.tabWidget.indexOf(self.mentionsTab),
                                     self.tr("@Me(%d)")
                                     % reminds['mention_status'])
            num_msg += 1

        if reminds['cmt'] and self.remindComments:
            msg += self.tr("%d unread comment(s)") % reminds['cmt'] + "\n"
            self.tabTextChanged.emit(self.tabWidget.indexOf(self.commentsTab),
                                     self.tr("Comments(%d)")
                                     % reminds['cmt'])
            num_msg += 1

        if num_msg:
            self.notify.showMessage(self.tr("WeCase"), msg)

    def setTabText(self, index, string):
        self.tabWidget.setTabText(index, string)

    def moveToTop(self):
        self.currentTweetView().moveToTop()

    def setLoaded(self):
        pass

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
        wecase_login = LoginWindow(allow_auto_login=False)
        wecase_login.exec_()

    def postTweet(self):
        wecase_new = NewpostWindow()
        wecase_new.exec_()

    def refresh(self):
        tweetView = self.currentTweetView()
        tweetView.model().timelineLoaded.connect(self.moveToTop)
        tweetView.refresh()
        self.reset_remind()

    def currentTweetView(self):
        # The most tricky part of MainWindow.
        # See MainWindow_ui.py for details.
        return self.tabWidget.currentWidget().layout().itemAt(0).widget()

    def closeEvent(self, event):
        self.timer.stop_event.set()
