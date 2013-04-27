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
        for tweetView in self.tweetViews:
            tweetView.setResizeMode(tweetView.SizeRootObjectToView)
            tweetView.setSource(
                QtCore.QUrl.fromLocalFile(const.myself_path + 
                                          "/ui/TweetList.qml"))
            tweetView.rootContext().setContextProperty("mainWindow", self)

    @QtCore.pyqtSlot()
    def load_more(self):
        model = self.get_current_model()
        model.next()

    def setupModels(self):
        self.all_timeline = TweetCommonModel(TweetItem(), 
                                             self.client.statuses.home_timeline,
                                             self)
        self.all_timeline.load()
        self.homeView.rootContext().setContextProperty("mymodel",
                                                       self.all_timeline)
        self.mentions = TweetCommonModel(TweetItem(),
                                         self.client.statuses.mentions,
                                         self)
        self.mentions.load()
        self.mentionsView.rootContext().setContextProperty("mymodel",
                                                           self.mentions)
        self.comment_to_me = TweetCommentModel(TweetItem(), 
                                               self.client.comments.to_me,
                                               self)
        self.comment_to_me.load()
        self.commentsView.rootContext().setContextProperty("mymodel",
                                                           self.comment_to_me)
        self.my_timeline = TweetCommonModel(TweetItem(),
                                            self.client.statuses.user_timeline,
                                            self)
        self.my_timeline.load()
        self.myView.rootContext().setContextProperty("mymodel",
                                                     self.my_timeline)

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
        self.get_current_tweetView().rootObject().positionViewAtBeginning()

    def setLoaded(self, tweetid):
        self.get_current_tweetView().rootObject().imageLoaded(tweetid)

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
        wecase_new = NewpostWindow()
        wecase_new.client = self.client
        wecase_new.exec_()

    @QtCore.pyqtSlot(str)
    def comment(self, idstr):
        wecase_new = NewpostWindow(action="comment", id=int(idstr))
        wecase_new.client = self.client
        wecase_new.exec_()

    @QtCore.pyqtSlot(str, str)
    def repost(self, idstr, text):
        wecase_new = NewpostWindow(action="retweet", id=int(idstr), text=text)
        wecase_new.client = self.client
        wecase_new.exec_()

    @QtCore.pyqtSlot(str, result=int)
    def favorite(self, idstr):
        try:
            self.client.favorites.create.post(id=int(idstr))
            return True
        except:
            return False

    @QtCore.pyqtSlot(str, result=bool)
    def un_favorite(self, idstr):
        try:
            self.client.favorites.destroy.post(id=int(idstr))
            return True
        except:
            return False

    @QtCore.pyqtSlot(str, str)
    def reply(self, idstr, cidstr):
        wecase_new = NewpostWindow(action="reply", id=int(idstr),
                                   cid=int(cidstr))
        wecase_new.client = self.client
        wecase_new.exec_()

    @QtCore.pyqtSlot(str, str)
    def look_orignal_pic(self, thumbnail_pic, tweetid):
        threading.Thread(group=None, target=self.fetch_open_original_pic,
                         args=(thumbnail_pic, tweetid)).start()

    def fetch_open_original_pic(self, thumbnail_pic, tweetid):
        """Fetch and open original pic from thumbnail pic url.
           Pictures will stored in cache directory. If we already have a same
           name in cache directory, just open it. If we don't, then download it
           first."""

        if tweetid in self.download_lock:
            return
        self.download_lock.append(tweetid)
        original_pic = thumbnail_pic.replace("thumbnail",
                                             "large")  # A simple trick ... ^_^
        localfile = const.cache_path + original_pic.split("/")[-1]
        if not os.path.exists(localfile):
            urllib.request.urlretrieve(original_pic, localfile)

        self.download_lock.remove(tweetid)
        os.popen("xdg-open " + localfile)  # xdg-open is common?
        self.imageLoaded.emit(tweetid)

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
