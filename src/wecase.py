#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client
# Since 4th,Feb,2013
# This is a TEST version
# Wait for ...
# Copyright: GPL v3 or later.

# Well, Let's go!


import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
import os
import urllib
import httplib
import shelve
from weibo import APIClient
from PyQt4 import QtCore, QtGui
from LoginWindow_ui import Ui_frm_Login
from MainWindow_ui import Ui_frm_MainWindow
from SettingWindow_ui import Ui_SettingWindow
from NewpostWindow_ui import Ui_NewPostWindow

APP_KEY = "1011524190"
APP_SECRET = "1898b3f668368b9f4a6f7ac8ed4a918f"
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
OAUTH2_PARAMETER = {'client_id':       APP_KEY,
                    'response_type':   'code',
                    'redirect_uri':    CALLBACK_URL,
                    'action':          'submit',
                    'userId':          '',  # username
                    'passwd':          '',  # password
                    'isLoginSina':     0,
                    'from':            '',
                    'regCallback':     '',
                    'state':           '',
                    'ticket':          '',
                    'withOfficalFlag': 0}
config_path = os.environ['HOME'] + '/.config/wecase/config_db'


class LoginWindow(QtGui.QWidget, Ui_frm_Login):
    passwd = {}
    last_login = ""
    auto_login = False

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.loadConfig()
        self.setupUi(self)
        self.setupMyUi()
        self.setupSignals()

    def setupSignals(self):
        self.pushButton_log.clicked.connect(self.non_block_login)
        self.chk_AutoLogin.clicked.connect(self.auto_login_clicked)
        QtCore.QObject.connect(self.cmb_Users, QtCore.SIGNAL("currentIndexChanged(QString)"), self.setPassword)

    def setupMyUi(self):
        self.txt_Password.setEchoMode(QtGui.QLineEdit.Password)
        self.cmb_Users.addItem(self.last_login)
        self.chk_AutoLogin.setChecked(self.auto_login)

        for username in self.passwd.keys():
            if username == self.last_login:
                continue
            self.cmb_Users.addItem(username)

        if self.cmb_Users.currentText():
            self.setPassword(self.cmb_Users.currentText())

        if self.auto_login:
            self.non_block_login()

    def loadConfig(self):
        self.config = shelve.open(config_path, 'c')
        try:
            self.passwd = self.config['passwd']
            self.last_login = self.config['last_login']
            self.auto_login = self.config['auto_login']
        except KeyError:
            pass

    def saveConfig(self):
        self.config['passwd'] = self.passwd
        self.config['last_login'] = self.last_login
        self.config['auto_login'] = self.chk_AutoLogin.isChecked()

    def non_block_login(self):
        # HACK: use a QTimer to login in another Thread
        self.login_timer = QtCore.QTimer()
        QtCore.QObject.connect(self.login_timer, QtCore.SIGNAL("timeout()"), self.login)
        self.login_timer.start(20)

    def login(self):
        self.login_timer.stop()

        self.username = self.cmb_Users.currentText()
        self.password = self.txt_Password.text()

        client = self.authorize(self.username, self.password)

        if client:
            if self.chk_Remember.isChecked():
                self.passwd[unicode(self.username)] = unicode(self.password)
                self.last_login = unicode(self.username)
                self.saveConfig()

            wecase_new.client = client
            wecase_main.client = client
            wecase_main.get_all_timeline()
            wecase_main.get_my_timeline()
            wecase_main.get_mentions_timeline()
            wecase_main.get_comment_to_me()
            wecase_main.show()
            self.close()
        else:
            QtGui.QMessageBox.critical(None, "Authorize Failed!",
                                       "Check your account and password!")

    def authorize(self, username, password):
        # TODO: This method is very messy, maybe do some cleanup?

        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,
                           redirect_uri=CALLBACK_URL)

        # Step 1: Get the authorize url from Sina
        authorize_url = client.get_authorize_url()

        # Step 2: Send the authorize info to Sina and get the authorize_code
        # TODO: Rewrite them with urllib/urllib2
        oauth2 = OAUTH2_PARAMETER
        oauth2['userId'] = username
        oauth2['passwd'] = password
        postdata = urllib.urlencode(oauth2)

        conn = httplib.HTTPSConnection('api.weibo.com')
        conn.request('POST', '/oauth2/authorize', postdata,
                     {'Referer':       authorize_url,
                      'Content-Type': 'application/x-www-form-urlencoded'})

        res = conn.getresponse()

        location = res.getheader('location')

        if not location:
            return None

        authorize_code = location.split('=')[1]
        conn.close()

        # Step 3: Put the authorize information into SDK
        r = client.request_access_token(authorize_code)
        access_token = r.access_token
        expires_in = r.expires_in

        client.set_access_token(access_token, expires_in)

        return client

    def setPassword(self, username):
        self.txt_Password.setText(self.passwd[unicode(username)])

    def auto_login_clicked(self):
        self.chk_Remember.setChecked(self.chk_AutoLogin.isChecked())


class WeCaseWindow(QtGui.QMainWindow, Ui_frm_MainWindow):
    client = None

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setupMyUi()
        self.setupSignals()
        self.setupModels()

    def setupMyUi(self):
        self.listView.setWordWrap(True)
        self.listView_2.setWordWrap(True)
        self.listView_3.setWordWrap(True)
        self.listView_4.setWordWrap(True)

    def setupSignals(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_Settings.triggered.connect(self.settings_show)
        self.action_Log_out.triggered.connect(self.logout)
        self.action_Refresh.triggered.connect(self.get_all_timeline)

        self.pushButton_settings.clicked.connect(self.settings_show)
        self.pushButton_refresh.clicked.connect(self.get_all_timeline)
        self.pushButton_new.clicked.connect(self.new_tweet)

    def setupModels(self):
        self.all_timeline = QtGui.QStandardItemModel(self)
        self.listView.setModel(self.all_timeline)
        self.mentions = QtGui.QStandardItemModel(self)
        self.listView_2.setModel(self.mentions)
        self.comment_to_me = QtGui.QStandardItemModel(self)
        self.listView_3.setModel(self.comment_to_me)
        self.my_timeline = QtGui.QStandardItemModel(self)
        self.listView_4.setModel(self.my_timeline)

    # XXX: get_all_timeline, get_my_timeline,
    # get_mentions_timeline, get_comment_to_me are almost same.
    # TODO: DRY! Write a new class for messages.

    def get_all_timeline(self):
        all_timelines = self.client.statuses.home_timeline.get().statuses
        for count, timeline in enumerate(all_timelines):
            item_content = QtGui.QStandardItem("%s\nAuthor: %s\nText: %s\n" %
                                               (timeline['created_at'],
                                                timeline['user']['name'],
                                                timeline['text']))
            item_id = QtGui.QStandardItem(timeline['idstr'])
            self.all_timeline.setItem(count, 0, item_content)
            self.all_timeline.setItem(count, 1, item_id)

    def get_my_timeline(self):
        my_timelines = self.client.statuses.user_timeline.get().statuses

        for count, timeline in enumerate(my_timelines):
            item_content = QtGui.QStandardItem("%s\nAuthor: %s\nText: %s\n" %
                                               (timeline['created_at'],
                                                timeline['user']['name'],
                                                timeline['text']))
            item_id = QtGui.QStandardItem(timeline['idstr'])
            self.my_timeline.setItem(count, 0, item_content)
            self.my_timeline.setItem(count, 1, item_id)


    def get_mentions_timeline(self):
        mentions_timelines = self.client.statuses.mentions.get().statuses

        for count, timeline in enumerate(mentions_timelines):
            item_content = QtGui.QStandardItem("%s\nAuthor: %s\nText: %s\n" %
                                                (timeline['created_at'],
                                                 timeline['user']['name'],
                                                 timeline['text']))
            item_id = QtGui.QStandardItem(timeline['idstr'])
            self.mentions.setItem(count, 0, item_content)
            self.mentions.setItem(count, 1, item_id)

    def get_comment_to_me(self):
        comments_to_me = self.client.comments.to_me.get().comments

        for count, comment in enumerate(comments_to_me):
            item_content = QtGui.QStandardItem("%s\nAuthor: %s\nText: %s\n" %
                                               (comment['created_at'],
                                                comment['user']['name'],
                                                comment['text']))
            item_id = QtGui.QStandardItem(comment['idstr'])
            self.comment_to_me.setItem(count, 0, item_content)
            self.comment_to_me.setItem(count, 1, item_id)

    def settings_show(self):
        wecase_settings.show()

    def logout(self):
        wecase_login.show()
        self.close()

    def new_tweet(self):
        wecase_new.show()


class WeSettingsWindow(QtGui.QWidget, Ui_SettingWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


class NewpostWindow(QtGui.QWidget, Ui_NewPostWindow):
    client = None
    image = None

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setupSignals()

    def setupSignals(self):
        self.pushButton_picture.clicked.connect(self.add_image)
        self.pushButton_send.clicked.connect(self.send_tweet)

    def send_tweet(self):
        text = unicode(self.textEdit.toPlainText())

        if self.image:
            self.client.statuses.upload.post(status=text, pic=open(self.image))
        else:
            self.client.statuses.update.post(status=text)

        self.image = None
        self.close()

    def add_image(self):
        if self.image:
            self.image = None
            self.pushButton_picture.setText("Picture")
        else:
            self.image = unicode(QtGui.QFileDialog.getOpenFileName(self, "Choose a image", filter="Images (*.png *.jpg *.bmp *.gif)"))
            self.pushButton_picture.setText("Remove the picture")


if __name__ == "__main__":
    try:
        os.mkdir(config_path.replace("/config_db", ""))
    except OSError:
        pass

    app = QtGui.QApplication(sys.argv)

    wecase_login = LoginWindow()
    wecase_main = WeCaseWindow()
    wecase_settings = WeSettingsWindow()
    wecase_new = NewpostWindow()

    wecase_login.show()
    sys.exit(app.exec_())
