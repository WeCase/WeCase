#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client
# Since 4th,Feb,2013
# This is a TEST version
# Wait for ...
# Copyright: GPL v3 or later.

# Well, Let's go!


import sys
import os
import re
import webbrowser
import urllib.request
import urllib.parse
import urllib.error
import http.client
from configparser import ConfigParser
import notify2 as pynotify
import threading
from WTimer import WTimer
from weibo import APIClient, APIError
from PyQt4 import QtCore, QtGui
from TweetUtils import tweetLength
from Tweet import TweetModel, TweetItem
from Smiley import SmileyModel, SmileyItem
from LoginWindow_ui import Ui_frm_Login
from MainWindow_ui import Ui_frm_MainWindow
from SettingWindow_ui import Ui_SettingWindow
from NewpostWindow_ui import Ui_NewPostWindow
from AboutWindow_ui import Ui_About_Dialog
from SmileyWindow_ui import Ui_SmileyWindow

APP_KEY = "1011524190"
APP_SECRET = "1898b3f668368b9f4a6f7ac8ed4a918f"
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
OAUTH2_PARAMETER = {'client_id': APP_KEY,
                    'response_type': 'code',
                    'redirect_uri': CALLBACK_URL,
                    'action': 'submit',
                    'userId': '',  # username
                    'passwd': '',  # password
                    'isLoginSina': 0,
                    'from': '',
                    'regCallback': '',
                    'state': '',
                    'ticket': '',
                    'withOfficalFlag': 0}
config_path = os.environ['HOME'] + '/.config/wecase/config_db'
cache_path = os.environ['HOME'] + '/.cache/wecase/'
myself_name = sys.argv[0].split('/')[-1]
myself_path = os.path.abspath(sys.argv[0]).replace(myself_name, "")


class LoginWindow(QtGui.QDialog, Ui_frm_Login):
    loginReturn = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.loadConfig()
        self.setupUi(self)
        self.setupMyUi()
        self.setupSignals()

    def setupSignals(self):
        # Other singals defined in Desinger.
        self.loginReturn.connect(self.checkLogin)
        self.chk_Remember.clicked.connect(self.uncheckAutoLogin)

    def accept(self, client):
        if self.chk_Remember.isChecked():
            self.passwd[str(self.username)] = str(self.password)
            self.last_login = str(self.username)
            # Because this is a model dislog,
            # closeEvent won't emit when we accept() the window, but will
            # emit when we reject() the window.
            self.saveConfig()
        wecase_main = WeCaseWindow()
        wecase_main.init_account(client)
        wecase_main.show()
        # Maybe users will logout, so reset the status
        self.pushButton_log.setText(self.tr("GO!"))
        self.pushButton_log.setEnabled(True)
        self.done(True)

    def reject(self):
        QtGui.QMessageBox.critical(None, self.tr("Authorize Failed!"),
                                   self.tr("Check your account and "
                                           "password!"))
        self.pushButton_log.setText(self.tr("GO!"))
        self.pushButton_log.setEnabled(True)

    def checkLogin(self, client):
        if client:
            self.accept(client)
        else:
            self.reject()

    def setupMyUi(self):
        self.show()
        self.txt_Password.setEchoMode(QtGui.QLineEdit.Password)
        self.cmb_Users.addItem(self.last_login)

        for username in list(self.passwd.keys()):
            if username == self.last_login:
                continue
            self.cmb_Users.addItem(username)

        if self.cmb_Users.currentText():
            self.chk_Remember.setChecked(True)
            self.setPassword(self.cmb_Users.currentText())

        if self.auto_login:
            self.chk_AutoLogin.setChecked(self.auto_login)
            self.login()

    def loadConfig(self):
        self.config = ConfigParser()
        self.config.read(config_path)

        if not self.config.has_section('login'):
            self.config['login'] = {}

        self.login_config = self.config['login']
        self.passwd = eval(self.login_config.get('passwd', "{}"))
        self.last_login = str(self.login_config.get('last_login', ""))
        self.auto_login = self.login_config.getboolean('auto_login', 0)

    def saveConfig(self):
        self.login_config['passwd'] = str(self.passwd)
        self.login_config['last_login'] = self.last_login
        self.login_config['auto_login'] = str(self.chk_AutoLogin.isChecked())

        with open(config_path, "w+") as config_file:
            self.config.write(config_file)

    def login(self):
        self.pushButton_log.setText(self.tr("Login, waiting..."))
        self.pushButton_log.setEnabled(False)
        self.ui_authorize()

    def ui_authorize(self):
        self.username = self.cmb_Users.currentText()
        self.password = self.txt_Password.text()
        threading.Thread(group=None, target=self.authorize,
                         args=(self.username, self.password)).start()

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
        postdata = urllib.parse.urlencode(oauth2)

        conn = http.client.HTTPSConnection('api.weibo.com')
        conn.request('POST', '/oauth2/authorize', postdata,
                     {'Referer': authorize_url,
                      'Content-Type': 'application/x-www-form-urlencoded'})

        res = conn.getresponse()

        location = res.getheader('location')

        if not location:
            return self.loginReturn.emit(None)

        authorize_code = location.split('=')[1]
        conn.close()

        # Step 3: Put the authorize information into SDK
        r = client.request_access_token(authorize_code)
        access_token = r.access_token
        expires_in = r.expires_in

        client.set_access_token(access_token, expires_in)
        self.loginReturn.emit(client)

    def setPassword(self, username):
        if username:
            self.txt_Password.setText(self.passwd[str(username)])

    @QtCore.pyqtSlot(bool)
    def uncheckAutoLogin(self, checked):
        if not checked:
            self.chk_AutoLogin.setChecked(False)

    def openRegisterPage(self):
        webbrowser.open("http://weibo.com/signup/signup.php")

    def closeEvent(self, event):
        # HACK: When a user want to close this window, closeEvent will emit.
        # But if we don't have closeEvent, Qt will call reject(). We use
        # reject() to show the error message, so users will see the error and
        # they can not close this window. So just do nothing there to allow
        # users to close the window.
        pass


class WeCaseWindow(QtGui.QMainWindow, Ui_frm_MainWindow):
    client = None
    uid = None
    timelineLoaded = QtCore.pyqtSignal(int)
    imageLoaded = QtCore.pyqtSignal(str)
    tabTextChanged = QtCore.pyqtSignal(int, str)

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.tweetViews = [self.homeView, self.mentionsView, self.commentsView,
                           self.myView]
        self.setupModels()
        self.setupMyUi()
        self.loadConfig()
        self.IMG_AVATAR = -2
        self.IMG_THUMB = -1
        self.notify = Notify(timeout=self.notify_timeout)
        self.applyConfig()

    def init_account(self, client):
        self.client = client
        self.get_uid()
        self.get_all_timeline()
        self.get_my_timeline()
        self.get_mentions_timeline()
        self.get_comment_to_me()

    def loadConfig(self):
        self.config = ConfigParser()
        self.config.read(config_path)

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
                QtCore.QUrl.fromLocalFile(myself_path + "/ui/TweetList.qml"))
            tweetView.rootContext().setContextProperty("mainWindow", self)

    @QtCore.pyqtSlot()
    def load_more(self):
        if self.tabWidget.currentIndex() == 0:
            self.all_timeline_page += 1
            self.get_all_timeline(self.all_timeline_page)
        elif self.tabWidget.currentIndex() == 1:
            self.mentions_page += 1
            self.get_mentions_timeline(self.mentions_page)
        elif self.tabWidget.currentIndex() == 2:
            self.comment_to_me_page += 1
            self.get_comment_to_me(self.comment_to_me_page)
        elif self.tabWidget.currentIndex() == 3:
            self.my_timeline_page += 1
            self.get_my_timeline(self.my_timeline_page)

    def setupModels(self):
        self.all_timeline = TweetModel(TweetItem(), self)
        self.homeView.rootContext().setContextProperty("mymodel",
                                                       self.all_timeline)
        self.mentions = TweetModel(TweetItem(), self)
        self.mentionsView.rootContext().setContextProperty("mymodel",
                                                           self.mentions)
        self.comment_to_me = TweetModel(TweetItem(), self)
        self.commentsView.rootContext().setContextProperty("mymodel",
                                                           self.comment_to_me)
        self.my_timeline = TweetModel(TweetItem(), self)
        self.myView.rootContext().setContextProperty("mymodel",
                                                     self.my_timeline)

    def get_timeline(self, timeline, model, more=False):
        for item in timeline:
            model.appendRow(TweetItem(item))
        self.timelineLoaded.emit(more)

    def get_all_timeline(self, page=1, reset_remind=False, more=False):
        all_timelines = self.client.statuses.home_timeline.get(
            page=page).statuses
        threading.Thread(group=None, target=self.get_timeline,
                         args=(all_timelines, self.all_timeline, more)).start()
        self.all_timeline_page = page
        if reset_remind:
            self.tabWidget.setTabText(0, self.tr("Weibo"))

    def get_my_timeline(self, page=1, reset_remind=False, more=False):
        my_timelines = self.client.statuses.user_timeline.get(
            page=page).statuses
        threading.Thread(group=None, target=self.get_timeline,
                         args=(my_timelines, self.my_timeline, more)).start()
        self.my_timeline_page = page

    def get_mentions_timeline(self, page=1, reset_remind=False, more=False):
        mentions_timelines = self.client.statuses.mentions.get(
            page=page).statuses
        threading.Thread(group=None, target=self.get_timeline,
                         args=(
                             mentions_timelines, self.mentions, more)).start()
        self.mentions_page = page
        if reset_remind:
            self.client.remind.set_count.post(type="mention_status")
            self.tabWidget.setTabText(1, self.tr("@ME"))

    def get_comment_to_me(self, page=1, reset_remind=False, more=False):
        comments_to_me = self.client.comments.to_me.get(page=page).comments
        threading.Thread(group=None, target=self.get_timeline, args=(
            comments_to_me, self.comment_to_me, more)).start()
        self.comment_to_me_page = page
        if reset_remind:
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
        msg = "You have:\n"
        num_msg = 0

        if reminds['status'] != 0:
            # Note: do NOT send notify here, or users will crazy.
            self.tabTextChanged.emit(0, self.tr("Weibo(%d)")
                                     % reminds['status'])

        if reminds['mention_status'] and self.remindMentions:
            msg += "%d unread @ME\n" % reminds['mention_status']
            self.tabTextChanged.emit(1, self.tr("@Me(%d)")
                                     % reminds['mention_status'])
            num_msg += 1

        if reminds['cmt'] and self.remindComments:
            msg += "%d unread comment(s)\n" % reminds['cmt']
            self.tabTextChanged.emit(2, self.tr("Comments(%d)")
                                     % reminds['cmt'])
            num_msg += 1

        if num_msg != 0:
            self.notify.showMessage(self.tr("WeCase"), msg)

    def setTabText(self, index, string):
        self.tabWidget.setTabText(index, string)

    def moveToTop(self, more):
        if more:
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
        # XXX: This function is NOT thread-safe!
        # Click a single picture for many time will download a image for many
        # times, and the picture may be overwrite, we will get a broken image.

        original_pic = thumbnail_pic.replace("thumbnail",
                                             "large")  # A simple trick ... ^_^
        localfile = cache_path + original_pic.split("/")[-1]
        if not os.path.exists(localfile):
            urllib.request.urlretrieve(original_pic, localfile)

        os.popen("xdg-open " + localfile)  # xdg-open is common?
        self.imageLoaded.emit(tweetid)

    def refresh(self):
        model = self.get_current_model()
        get_timeline = self.get_current_function()

        model.clear()
        threading.Thread(group=None, target=get_timeline,
                         args=(1, True, True)).start()

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


class WeSettingsWindow(QtGui.QDialog, Ui_SettingWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
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
        self.config.read(config_path)

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
        self.config.read(config_path)

        if not self.config.has_section('main'):
            self.config['main'] = {}

        self.main_config = self.config['main']
        self.main_config['notify_interval'] = str(self.intervalSlider.value())
        self.main_config['notify_timeout'] = str(self.timeoutSlider.value())
        self.main_config['remind_comments'] = str(self.commentsChk.isChecked())
        self.main_config['remind_mentions'] = str(self.mentionsChk.isChecked())

        with open(config_path, "w+") as config_file:
            self.config.write(config_file)

    def accept(self):
        self.saveConfig()
        self.done(True)

    def reject(self):
        self.done(False)


class NewpostWindow(QtGui.QDialog, Ui_NewPostWindow):
    client = None
    image = None
    apiError = QtCore.pyqtSignal(str)
    sendSuccessful = QtCore.pyqtSignal()

    def __init__(self, parent=None, action="new", id=None, cid=None, text=""):
        QtGui.QDialog.__init__(self, parent)
        self.action = action
        self.id = id
        self.cid = cid
        self.setupUi(self)
        self.setupMyUi()
        self.textEdit.setText(text)
        self.textEdit.callback = self.mentions_suggest
        self.textEdit.mention_flag = "@"
        self.notify = Notify(timeout=1)

    def setupMyUi(self):
        self.checkChars()
        if self.action == "new":
            self.chk_repost.setEnabled(False)
            self.chk_comment.setEnabled(False)
            self.chk_comment_original.setEnabled(False)
        elif self.action == "retweet":
            self.chk_repost.setEnabled(False)
        elif self.action == "comment":
            self.chk_comment.setEnabled(False)
        elif self.action == "reply":
            self.chk_repost.setEnabled(False)
            self.chk_comment.setEnabled(False)

    def mentions_suggest(self, text):
        ret_users = []
        try:
            word = re.findall('@[-a-zA-Z0-9_\u4e00-\u9fa5]+', text)[-1].replace('@', '')
        except IndexError:
            return []
        if not word.strip():
            return []
        users = self.client.search.suggestions.at_users.get(q=word, type=0)
        for user in users:
            ret_users.append("@" + user['nickname'])
        return ret_users

    def send(self):
        self.pushButton_send.setEnabled(False)
        if self.action == "new":
            threading.Thread(group=None, target=self.new).start()
        elif self.action == "retweet":
            threading.Thread(group=None, target=self.retweet).start()
        elif self.action == "comment":
            threading.Thread(group=None, target=self.comment).start()
        elif self.action == "reply":
            threading.Thread(group=None, target=self.reply).start()

    def retweet(self):
        text = str(self.textEdit.toPlainText())
        try:
            self.client.statuses.repost.post(id=int(self.id), status=text,
                                             is_comment=int((self.chk_comment.isChecked() +
                                             self.chk_comment_original.isChecked() * 2)))
            self.notify.showMessage(self.tr("WeCase"),
                                    self.tr("Retweet Success!"))
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

    def comment(self):
        text = str(self.textEdit.toPlainText())
        try:
            self.client.comments.create.post(id=int(self.id), comment=text,
                                             comment_ori=int(self.chk_comment_original.isChecked()))
            if self.chk_repost.isChecked():
                self.client.statuses.repost.post(id=int(self.id), status=text)
            self.notify.showMessage(self.tr("WeCase"),
                                    self.tr("Comment Success!"))
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

    def reply(self):
        text = str(self.textEdit.toPlainText())
        try:
            self.client.comments.reply.post(id=int(self.id), cid=int(self.cid),
                                            comment=text,
                                            comment_ori=int(self.chk_comment_original.isChecked()))
            if self.chk_repost.isChecked():
                self.client.statuses.repost.post(id=int(self.id), status=text)
            self.notify.showMessage(self.tr("WeCase"),
                                    self.tr("Reply Success!"))
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

    def new(self):
        text = str(self.textEdit.toPlainText())

        try:
            if self.image:
                self.client.statuses.upload.post(status=text,
                                                 pic=open(self.image, "rb"))
            else:
                self.client.statuses.update.post(status=text)

            self.notify.showMessage(self.tr("WeCase"),
                                    self.tr("Tweet Success!"))
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

        self.image = None

    def addImage(self):
        ACCEPT_TYPE = self.tr("Images") + "(*.png *.jpg *.bmp *.gif)"
        if self.image:
            self.image = None
            self.pushButton_picture.setText(self.tr("Picture"))
        else:
            self.image = QtGui.QFileDialog.getOpenFileName(self,
                                                           self.tr("Choose a"
                                                           " image"),
                                                           filter=ACCEPT_TYPE)
            self.pushButton_picture.setText(self.tr("Remove the picture"))

    def showError(self, e):
        if "Text too long" in e:
            QtGui.QMessageBox.warning(None, self.tr("Text too long!"),
                                      self.tr("Please remove some text."))
        else:
            QtGui.QMessageBox.warning(None, self.tr("Unknown error!"), e)
        self.pushButton_send.setEnabled(True)

    def showSmiley(self):
        wecase_smiley = SmileyWindow()
        if wecase_smiley.exec_():
            self.textEdit.textCursor().insertText(wecase_smiley.smileyName)

    def checkChars(self):
        '''Check textEdit's characters.
        If it larger than 140, Send Button will be disabled
        and label will show red chars.'''

        text = self.textEdit.toPlainText()
        numLens = 140 - tweetLength(text)
        if numLens == 140 and (not self.action == "retweet"):
            # you can not send empty tweet, except retweet
            self.pushButton_send.setEnabled(False)
        elif numLens >= 0:
            # length is okay
            self.label.setStyleSheet("color:black;")
            self.pushButton_send.setEnabled(True)
        else:
            # text is too long
            self.label.setStyleSheet("color:red;")
            self.pushButton_send.setEnabled(False)
        self.label.setText(str(numLens))


class Notify():
    image = myself_path + "/ui/img/WeCase 80.png"

    def __init__(self, appname=QtCore.QObject().tr("WeCase"), timeout=5):
        pynotify.init(appname)
        self.timeout = timeout
        self.n = pynotify.Notification(appname)

    def showMessage(self, title, text):
        self.n.update(title, text, self.image)
        self.n.set_timeout(self.timeout * 1000)
        self.n.show()


class AboutWindow(QtGui.QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


class SmileyWindow(QtGui.QDialog, Ui_SmileyWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setupMyUi()
        self.setupModels()
        self.smileyName = ""

    def setupMyUi(self):
        self.smileyView.setResizeMode(self.smileyView.SizeRootObjectToView)

    def setupModels(self):
        self.smileyModel = SmileyModel(self)
        self.smileyModel.init_smileies(myself_path + "./ui/img/smiley",
                                       self.smileyModel, SmileyItem)
        self.smileyView.rootContext().setContextProperty("SmileyModel",
                                                         self.smileyModel)
        self.smileyView.rootContext().setContextProperty("parentWindow", self)
        self.smileyView.setSource(QtCore.QUrl.fromLocalFile(
                                  myself_path + "/ui/SmileyView.qml"))

    @QtCore.pyqtSlot(str)
    def returnSmileyName(self, smileyName):
        self.smileyName = smileyName
        self.done(True)


if __name__ == "__main__":
    try:
        os.mkdir(config_path.replace("/config_db", ""))
    except OSError:
        pass

    try:
        os.mkdir(cache_path)
    except OSError:
        pass

    app = QtGui.QApplication(sys.argv)

    # Qt's built-in string translator
    qt_translator = QtCore.QTranslator(app)
    qt_translator.load("qt_" + QtCore.QLocale.system().name(),
                       QtCore.QLibraryInfo.location(
                       QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(qt_translator)

    # WeCase's own string translator
    my_translator = QtCore.QTranslator(app)
    my_translator.load("WeCase_" + QtCore.QLocale.system().name(),
                       myself_path + "locale")
    app.installTranslator(my_translator)

    wecase_login = LoginWindow()

    exit_status = app.exec_()

    # Cleanup code here.

    sys.exit(exit_status)
