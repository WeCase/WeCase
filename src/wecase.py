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
import notify2  # you should install python-notify2
import thread
from weibo import APIClient, APIError
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
cache_path = os.environ['HOME'] + '/.cache/wecase/'


class LoginWindow(QtGui.QDialog, Ui_frm_Login):
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
        self.pushButton_log.setText("Login, waiting...")
        self.pushButton_log.setEnabled(False)
        self.login_timer.stop()

        self.username = self.cmb_Users.currentText()
        self.password = self.txt_Password.text()

        client = self.authorize(self.username, self.password)

        if client:
            if self.chk_Remember.isChecked():
                self.passwd[unicode(self.username)] = unicode(self.password)
                self.last_login = unicode(self.username)
                self.saveConfig()

            wecase_main.client = client
            wecase_main.get_uid()
            wecase_main.get_all_timeline()
            wecase_main.get_my_timeline()
            wecase_main.get_mentions_timeline()
            wecase_main.get_comment_to_me()
            wecase_main.show()
            self.close()
        else:
            QtGui.QMessageBox.critical(None, "Authorize Failed!",
                                       "Check your account and password!")
        self.pushButton_log.setText("GO!")
        self.pushButton_log.setEnabled(True)

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
    uid = None

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.listViews = [self.listView, self.listView_2, self.listView_3, self.listView_4]
        self.setupMyUi()
        self.setupSignals()
        self.setupModels()
        self.IMG_AVATOR = -2
        self.IMG_THUMB = -1
        self.TIMER_INTERVAL = 30  # TODO:30 Seconds by default, can be modify with settings window
        self.notify = Notify()
        thread.start_new_thread(self.timer.start, (self.TIMER_INTERVAL * 1000, ))  # it can run in a new thread

    def setupMyUi(self):
        self.delegate = TweetDelegate()
        for listView in self.listViews:
            listView.setWordWrap(True)
            listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            listView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            listView.setItemDelegate(self.delegate)
        self.timer = QtCore.QTimer()  # check new unread_count

    def setupSignals(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_Settings.triggered.connect(self.settings_show)
        self.action_Log_out.triggered.connect(self.logout)
        self.action_Refresh.triggered.connect(self.refresh)

        #self.pushButton_settings.clicked.connect(self.settings_show)
        self.pushButton_refresh.clicked.connect(self.refresh)
        self.pushButton_new.clicked.connect(self.new_tweet)

        for listView in self.listViews:
            listView.connect(listView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.general_context)
            listView.verticalScrollBar().connect(listView.verticalScrollBar(), QtCore.SIGNAL("valueChanged(int)"), self.load_more)

        self.listView_3.connect(self.listView_3, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.comments_context)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.show_notify)

    def load_more(self, value):
        listView = self.get_current_listView()
        max_value = listView.verticalScrollBar().maximum()

        if value < max_value:
            return

        if self.tabWidget.currentIndex() == 0:
            self.all_timeline_page += 1
            thread.start_new_thread(self.get_all_timeline, (self.all_timeline_page, ))
        elif self.tabWidget.currentIndex() == 1:
            self.mentions_page += 1
            thread.start_new_thread(self.get_mentions_timeline, (self.mentions_page, ))
        elif self.tabWidget.currentIndex() == 2:
            self.comment_to_me_page += 1
            thread.start_new_thread(self.get_comment_to_me, (self.comment_to_me_page, ))
        elif self.tabWidget.currentIndex() == 3:
            self.my_timeline_page += 1
            thread.start_new_thread(self.get_my_timeline, (self.my_timeline_page, ))

    def setupModels(self):
        self.all_timeline = QtGui.QStandardItemModel(self)
        self.listView.setModel(self.all_timeline)
        self.mentions = QtGui.QStandardItemModel(self)
        self.listView_2.setModel(self.mentions)
        self.comment_to_me = QtGui.QStandardItemModel(self)
        self.listView_3.setModel(self.comment_to_me)
        self.my_timeline = QtGui.QStandardItemModel(self)
        self.listView_4.setModel(self.my_timeline)

    def get_timeline(self, timeline, model):
        def prefetchImage(url, img_type=-2):
            filename = url.split("/")[img_type]

            if not os.path.exists(cache_path + filename):
                urllib.urlretrieve(url, cache_path + filename)
            return

        rowCount = model.rowCount()

        for count_this_time, item in enumerate(timeline):
            count = rowCount + count_this_time
            prefetchImage(item['user']['profile_image_url'], self.IMG_AVATOR)

            # tweet (default), comment or retweet?
            item_type = QtGui.QStandardItem("tweet")

            # simple tweet or comment
            item_id = QtGui.QStandardItem(item['idstr'])
            item_author = QtGui.QStandardItem(item['user']['name'])
            item_author_avator = QtGui.QStandardItem(item['user']['profile_image_url'])
            item_content = QtGui.QStandardItem(item['text'])
            item_content_time = QtGui.QStandardItem(item['created_at'])

            # comment only
            try:
                item_comment_to_original_id = QtGui.QStandardItem(item['status']['idstr'])
                item_type = QtGui.QStandardItem("comment")
            except KeyError:
                # not a comment
                pass

            # original tweet (if retweeted)
            try:
                item_original_id = QtGui.QStandardItem(item['retweeted_status']['idstr'])
                item_original_content = QtGui.QStandardItem(item['retweeted_status']['text'])
                item_original_author = QtGui.QStandardItem(item['retweeted_status']['user']['name'])
                item_original_time = QtGui.QStandardItem(item['retweeted_status']['created_at'])
                item_type = QtGui.QStandardItem("retweet")
            except KeyError:
                # not retweeted
                pass

            # thumb pic
            try:
                item_thumb_pic = None
                prefetchImage(item['thumbnail_pic'], self.IMG_THUMB)
                item_thumb_pic = QtGui.QStandardItem(item['thumbnail_pic'])
            except KeyError:
                try:
                    prefetchImage(item['retweeted_status']['thumbnail_pic'], self.IMG_THUMB)
                    item_thumb_pic = QtGui.QStandardItem(item['retweeted_status']['thumbnail_pic'])
                except KeyError:
                    pass

            # tweet
            model.setItem(count, 0, item_type)
            model.setItem(count, 1, item_id)
            model.setItem(count, 2, item_author)
            model.setItem(count, 3, item_author_avator)
            model.setItem(count, 4, item_content)
            model.setItem(count, 5, item_content_time)

            if item_type.text() == "comment":
                # comment
                model.setItem(count, 6, item_comment_to_original_id)

            if item_type.text() == "retweet":
                # retweet
                model.setItem(count, 7, item_original_id)
                model.setItem(count, 8, item_original_content)
                model.setItem(count, 9, item_original_author)
                model.setItem(count, 10, item_original_time)

            if not item_thumb_pic is None:
                # thumb pic
                model.setItem(count, 11, item_thumb_pic)

            # process UI's event when we get every two item, or UI will freeze.
            if count_this_time % 2 == 0:
                app.processEvents()

    def get_all_timeline(self, page=1):
        all_timelines = self.client.statuses.home_timeline.get(page=page).statuses
        self.get_timeline(all_timelines, self.all_timeline)
        self.all_timeline_page = page
        self.tabWidget.setTabText(0, "Weibo")

    def get_my_timeline(self, page=1):
        my_timelines = self.client.statuses.user_timeline.get(page=page).statuses
        self.get_timeline(my_timelines, self.my_timeline)
        self.my_timeline_page = page

    def get_mentions_timeline(self, page=1):
        mentions_timelines = self.client.statuses.mentions.get(page=page).statuses
        self.get_timeline(mentions_timelines, self.mentions)
        self.mentions_page = page
        self.tabWidget.setTabText(1, "@ME")

    def get_comment_to_me(self, page=1):
        comments_to_me = self.client.comments.to_me.get(page=page).comments
        self.get_timeline(comments_to_me, self.comment_to_me)
        self.comment_to_me_page = page
        self.tabWidget.setTabText(2, "Comments")

    def get_remind(self, uid):
        '''this function is used to get unread_count
        from Weibo API. uid is necessary.'''

        reminds = self.client.remind.unread_count.get(uid=uid)
        return reminds

    def get_uid(self):
        '''How can I get my uid? here it is'''
        try:
            self.uid = self.client.account.get_uid.get().uid
        except AttributeError as err:
            return None

    def show_notify(self):
        reminds = self.get_remind(self.uid)
        msg = "You have:\n"
        num_msg = 0
        # TODO:we need settings window, to controll their displaying or not
        if reminds['status'] != 0:
            msg += "%d unread message(s)\n" % reminds['status']
            self.tabWidget.setTabText(0, "Weibo(%d)" % reminds['status'])
            num_msg += 1

        if reminds['mention_status'] != 0:
            msg += "%d unread @ME\n" % reminds['mention_status']
            self.tabWidget.setTabText(1, "@Me(%d)" % reminds['mention_status'])
            num_msg += 1

        if reminds['cmt'] != 0:
            msg += "%d unread comment(s)\n" % reminds['cmt']
            self.tabWidget.setTabText(2, "Comments(%d)" % reminds['cmt'])
            num_msg += 1

        if num_msg != 0:
            self.notify.showMessage("WeCase", msg, image="notification-message-email")  # TODO:image can use our images in rcc

    def settings_show(self):
        wecase_settings.show()

    def logout(self):
        wecase_login.show()
        self.close()

    def new_tweet(self):
        wecase_new = NewpostWindow()
        wecase_new.client = self.client
        wecase_new.exec_()

    def general_context(self, point):
        general_menu = QtGui.QMenu("Menu", self)

        action_Comment = QtGui.QAction("Comment", self)
        action_Repost = QtGui.QAction("Repost", self)
        action_Favorite = QtGui.QAction("Favorite", self)
        action_Un_Favorite = QtGui.QAction("Un-Favorite", self)

        action_Comment.triggered.connect(self.comment)
        action_Repost.triggered.connect(self.repost)
        action_Favorite.triggered.connect(self.favorite)
        action_Un_Favorite.triggered.connect(self.un_favorite)

        general_menu.addAction(action_Comment)
        general_menu.addAction(action_Repost)
        general_menu.addAction(action_Favorite)
        general_menu.addAction(action_Un_Favorite)

        # Show the context menu.
        listView = self.get_current_listView()
        if listView != self.listView_3:
            general_menu.exec_(listView.mapToGlobal(point))

    def comments_context(self, point):
        comment_menu = QtGui.QMenu("Menu", self)
        action_Reply = QtGui.QAction("Reply", self)
        action_Reply.triggered.connect(self.reply)
        comment_menu.addAction(action_Reply)
        comment_menu.exec_(self.listView_3.mapToGlobal(point))

    def comment(self):
        listView = self.get_current_listView()
        model = self.get_current_model()

        row = listView.currentIndex().row()
        idstr = model.item(row, 1).text()

        wecase_new = NewpostWindow(action="comment", id=int(idstr))
        wecase_new.client = self.client
        wecase_new.exec_()

    def repost(self):
        listView = self.get_current_listView()
        model = self.get_current_model()

        row = listView.currentIndex().row()
        idstr = model.item(row, 1).text()
        if model.item(row, 0).text() == "retweet":
            text = "//@%s: %s" % (model.item(row, 2).text(), model.item(row, 4).text())
        else:
            text = ""

        wecase_new = NewpostWindow(action="retweet", id=int(idstr), text=text)
        wecase_new.client = self.client
        wecase_new.exec_()

    def favorite(self):
        listView = self.get_current_listView()
        model = self.get_current_model()

        row = listView.currentIndex().row()
        idstr = model.item(row, 1).text()

        self.client.favorites.create.post(id=int(idstr))

    def un_favorite(self):
        listView = self.get_current_listView()
        model = self.get_current_model()

        row = listView.currentIndex().row()
        idstr = model.item(row, 1).text()

        self.client.favorites.destroy.post(id=int(idstr))

    def reply(self):
        row = self.listView_3.currentIndex().row()
        idstr = self.comment_to_me.item(row, 6).text()
        cidstr = self.comment_to_me.item(row, 1).text()

        wecase_new = NewpostWindow(action="reply", id=int(idstr), cid=int(cidstr))
        wecase_new.client = self.client
        wecase_new.exec_()

    def refresh(self):
        model = self.get_current_model()
        get_timeline = self.get_current_function()

        model.clear()
        get_timeline(page=1)

    def get_current_listView(self):
        listviews = {0: self.listView, 1: self.listView_2, 2: self.listView_3, 3: self.listView_4}
        return listviews[self.tabWidget.currentIndex()]

    def get_current_model(self):
        models = {0: self.all_timeline, 1: self.mentions, 2: self.comment_to_me, 3: self.my_timeline}
        return models[self.tabWidget.currentIndex()]

    def get_current_function(self):
        functions = {0: self.get_all_timeline, 1: self.get_mentions_timeline, 2: self.get_comment_to_me, 3: self.get_my_timeline}
        return functions[self.tabWidget.currentIndex()]


class WeSettingsWindow(QtGui.QDialog, Ui_SettingWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


class NewpostWindow(QtGui.QDialog, Ui_NewPostWindow):
    client = None
    image = None

    def __init__(self, parent=None, action="new", id=None, cid=None, text=""):
        QtGui.QWidget.__init__(self, parent)
        self.action = action
        self.id = id
        self.cid = cid
        self.setupUi(self)
        self.textEdit.setText(text)
        self.check_chars()
        self.setupSignals()
        self.notify = Notify(time=1)

    def setupMyUi(self):
        if self.action == "new":
            self.pushButton_send.clicked.connect(self.send_tweet)

    def setupSignals(self):
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_picture.clicked.connect(self.add_image)
        self.textEdit.textChanged.connect(self.check_chars)
        if self.action == "new":
            self.pushButton_send.clicked.connect(self.send_tweet)
        elif self.action == "retweet":
            self.pushButton_send.clicked.connect(self.retweet)
        elif self.action == "comment":
            self.pushButton_send.clicked.connect(self.comment)
        elif self.action == "reply":
            self.pushButton_send.clicked.connect(self.reply)

    def retweet(self):
        text = unicode(self.textEdit.toPlainText())
        try:
            self.client.statuses.repost.post(id=int(self.id), status=text)
            self.notify.showMessage("WeCase", "Retweet Success!")
        except APIError as e:
            self.error(e)
            return

        self.close()

    def comment(self):
        text = unicode(self.textEdit.toPlainText())
        try:
            self.client.comments.create.post(id=int(self.id), comment=text)
            self.notify.showMessage("WeCase", "Comment Success!")
        except APIError as e:
            self.error(e)
            return

        self.close()

    def reply(self):
        text = unicode(self.textEdit.toPlainText())
        try:
            self.client.comments.reply.post(id=int(self.id), cid=int(self.cid), comment=text)
            self.notify.showMessage("WeCase", "Reply Success!")
        except APIError as e:
            self.error(e)
            return

        self.close()

    def send_tweet(self):
        text = unicode(self.textEdit.toPlainText())

        try:
            if self.image:
                self.client.statuses.upload.post(status=text, pic=open(self.image))
            else:
                self.client.statuses.update.post(status=text)

            self.notify.showMessage("WeCase", "Tweet Success!")
        except APIError as e:
            self.error(e)
            return

        self.image = None
        self.close()

    def add_image(self):
        if self.image:
            self.image = None
            self.pushButton_picture.setText("Picture")
        else:
            self.image = unicode(QtGui.QFileDialog.getOpenFileName(self, "Choose a image", filter="Images (*.png *.jpg *.bmp *.gif)"))
            self.pushButton_picture.setText("Remove the picture")

    def error(self, e):
        e = unicode(e)
        if "Text too long" in e:
            QtGui.QMessageBox.warning(None, "Text too long!",
                                      "Please remove some text.")
        else:
            QtGui.QMessageBox.warning(None, "Unknown error!", e)

    def check_chars(self):
        '''Check textEdit's characters.
        If it larger than 140, Send Button will be disabled
        and label will show red chars.'''

        text = unicode(self.textEdit.toPlainText())
        numLens = 140 - len(text)
        if numLens >= 0:
            self.label.setStyleSheet("color:black;")
            self.pushButton_send.setEnabled(True)
        else:
            self.label.setStyleSheet("color:red;")
            self.pushButton_send.setEnabled(False)
        self.label.setText(str(numLens))


class TweetRendering(QtGui.QStyledItemDelegate):
    def __init__(self):
        QtGui.QStyledItemDelegate.__init__(self)
        self.IMG_AVATOR = -2  # type avator
        self.IMG_THUMB = -1   # type thumbnail image

    def loadImage(self, url, img_type=-2):
        # image has been prefetched, so just load it
        filename = url.split("/")[img_type]
        pixmap = QtGui.QPixmap(cache_path + filename)
        return pixmap

    def paint(self, painter, option, index):
        # some initializations for rendering
        options = QtGui.QStyleOptionViewItemV4(option)
        self.initStyleOption(options, index)
        options.text = ""  # remove the original text, render our own text
        style = QtGui.QApplication.style() if options.widget is None else options.widget.style()
        style.drawControl(QtGui.QStyle.CE_ItemViewItem, options, painter)

        # get data from model
        typ              = index.model().index(index.row(),  0).data().toString()
        author           = index.model().index(index.row(),  2).data().toString()
        author_avator    = index.model().index(index.row(),  3).data().toString()
        content          = index.model().index(index.row(),  4).data().toString()
        content_time     = index.model().index(index.row(),  5).data().toString()
        original_content = index.model().index(index.row(),  8).data().toString()
        original_author  = index.model().index(index.row(),  9).data().toString()
        original_time    = index.model().index(index.row(), 10).data().toString()
        thumbnail_pic    = index.model().index(index.row(), 11).data().toString()  # get thubmnail_pic

        # position for rendering
        # textRect = style.subElementRect(QtGui.QStyle.SE_ItemViewItemText, options)
        # Can not get correct position under Oxygen.
        # Maybe a bug (KDE #315428), but can not comfirm now.
        # So that's a workaround from a KDE developer.
        textRect = options.rect

        # draw avator
        painter.save()
        avator = self.loadImage(str(author_avator), self.IMG_AVATOR)
        avator = avator.scaled(32, 32)
        painter.drawPixmap(textRect.topLeft() + QtCore.QPoint(2, 4), avator)
        painter.restore()

        # draw author's name
        painter.save()
        painter.translate(textRect.left() + 32, textRect.top() + 1)
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc = QtGui.QTextDocument()
        doc.setHtml(author)
        doc.setTextWidth(option.rect.width())
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        doc.documentLayout().draw(painter, ctx)
        painter.restore()

        # draw time
        painter.save()
        painter.translate(textRect.left() + 32, textRect.top() + 16 + 1)
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc = QtGui.QTextDocument()
        doc.setHtml(content_time)
        doc.setTextWidth(option.rect.width())
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        doc.documentLayout().draw(painter, ctx)
        painter.restore()

        # draw content
        painter.save()
        painter.translate(textRect.left() + 32, textRect.top() + 16 + 1 + 16)
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc = QtGui.QTextDocument()
        doc.setHtml(content)
        doc.setTextWidth(option.rect.width() - 50)
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        doc.documentLayout().draw(painter, ctx)
        content_height = doc.size().height()
        content_width = doc.size().width()
        painter.restore()

        # draw original content (if retweeted)
        if typ == "retweet":
            painter.save()
            painter.translate(textRect.left() + 32 + 32, textRect.top() + content_height + 16 + 1 + 16)
            painter.setClipRect(textRect.translated(-textRect.topLeft()))
            doc = QtGui.QTextDocument()
            doc.setHtml("@%s: %s" % (original_author, original_content))
            doc.setTextWidth(option.rect.width() - 82)
            ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
            doc.documentLayout().draw(painter, ctx)
            content_height += doc.size().height()
            painter.restore()

        # Show picture
        if thumbnail_pic != "":
            painter.save()
            thumb = self.loadImage(str(thumbnail_pic), self.IMG_THUMB)
            center_left = (content_width - thumb.width()) / 2
            painter.drawPixmap(textRect.topLeft() + QtCore.QPoint(center_left, content_height + 16 + 1 + 16), thumb)
            painter.restore()

    def sizeHint(self, option, index):
        # some initializations for rendering
        options = QtGui.QStyleOptionViewItemV4(option)
        self.initStyleOption(options, index)
        options.text = ""  # remove the original text, render our own text

        height = 0

        # get data from model
        typ              = index.model().index(index.row(), 0).data().toString()
        content          = index.model().index(index.row(), 4).data().toString()
        original_content = index.model().index(index.row(), 8).data().toString()
        original_author  = index.model().index(index.row(), 9).data().toString()
        thumbnail_pic    = index.model().index(index.row(), 11).data().toString()  # get thubmnail_pic

        # author's name
        height += 1

        # time
        height += 16

        # content
        height += 16
        doc = QtGui.QTextDocument()
        doc.setHtml(content)
        doc.setTextWidth(option.rect.width())
        height += doc.size().height()
        content_width = doc.size().width()

        # HACK: extra space
        height += 10

        # draw original content (if retweeted)
        if typ == "retweet":
            height += 16
            doc.setHtml("@%s: %s" % (original_author, original_content))
            doc.setTextWidth(option.rect.width() - 82)
            height += doc.size().height()
            content_width = doc.size().width()

        # show pic
        if thumbnail_pic != "":
            height += 16
            thumb = self.loadImage(str(thumbnail_pic), self.IMG_THUMB)
            height += thumb.height()

        return content_width, height


class TweetDelegate(QtGui.QStyledItemDelegate):
    def __init__(self):
        QtGui.QStyledItemDelegate.__init__(self)

    def paint(self, painter, option, index):
        tweet = TweetRendering()
        tweet.paint(painter, option, index)

    def sizeHint(self, option, index):
        tweet = TweetRendering()
        width, height = tweet.sizeHint(option, index)

        return QtCore.QSize(width, height)


class Notify():
    def __init__(self, appname="WeCase", time=5):
        notify2.init(appname)
        self.timeout = time
        self.n = notify2.Notification(appname)

    def showMessage(self, title, text, image=""):
        self.n.update(title, text, image)
        self.n.set_timeout(self.timeout * 1000)  # TODO:user should be able to adjust the time by settings window
        self.n.show()

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

    wecase_login = LoginWindow()
    wecase_main = WeCaseWindow()
    wecase_settings = WeSettingsWindow()

    wecase_login.show()
    sys.exit(app.exec_())
