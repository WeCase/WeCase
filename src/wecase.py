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
        self.listViews = [self.listView, self.listView_2, self.listView_3, self.listView_4]
        self.setupMyUi()
        self.setupSignals()
        self.setupModels()

    def setupMyUi(self):
        self.delegate = HTMLDelegate()
        for listView in self.listViews:
            listView.setWordWrap(True)
            listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            listView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            listView.setItemDelegate(self.delegate)
            listView.setSpacing(3)

    def setupSignals(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_Settings.triggered.connect(self.settings_show)
        self.action_Log_out.triggered.connect(self.logout)
        self.action_Refresh.triggered.connect(self.refresh)

        self.pushButton_settings.clicked.connect(self.settings_show)
        self.pushButton_refresh.clicked.connect(self.refresh)
        self.pushButton_new.clicked.connect(self.new_tweet)

        for listView in self.listViews:
            listView.connect(listView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.general_context)
            listView.verticalScrollBar().connect(listView.verticalScrollBar(), QtCore.SIGNAL("valueChanged(int)"), self.load_more)

        self.listView_3.connect(self.listView_3, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.comments_context)

    def load_more(self, value):
        listView = self.get_current_listView()
        max_value = listView.verticalScrollBar().maximum()

        if value < max_value:
            return

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
        self.all_timeline = QtGui.QStandardItemModel(self)
        self.listView.setModel(self.all_timeline)
        self.mentions = QtGui.QStandardItemModel(self)
        self.listView_2.setModel(self.mentions)
        self.comment_to_me = QtGui.QStandardItemModel(self)
        self.listView_3.setModel(self.comment_to_me)
        self.my_timeline = QtGui.QStandardItemModel(self)
        self.listView_4.setModel(self.my_timeline)

    def get_timeline(self, timeline, model):
        rowCount = model.rowCount()
        for count_this_time, item in enumerate(timeline):
            count = rowCount + count_this_time
            try:
                item_content = QtGui.QStandardItem("%s<br>Author: %s<br>Text: %s<br>↘<br>" %
                                (item['created_at'], item['user']['name'], item['text'])
                                + "    Time: %s<br>    Author: %s<br>    Text: %s<br>" %
                                (item['retweeted_status']['created_at'], item['retweeted_status']['user']['name'],
                                 item['retweeted_status']['text']))
                item_source_id = QtGui.QStandardItem(item['status']['idstr'])
            except KeyError:
                item_content = QtGui.QStandardItem("%s<br>Author: %s<br>Text: %s<br>" %
                                               (item['created_at'], item['user']['name'], item['text']))
                item_source_id = QtGui.QStandardItem("")

            item_id = QtGui.QStandardItem(item['idstr'])

            model.setItem(count, 0, item_content)
            model.setItem(count, 1, item_id)
            model.setItem(count, 2, item_source_id)

            # process UI's event, or UI will freeze.
            if count_this_time % 2 == 0:
                app.processEvents()

    def get_all_timeline(self, page=1):
        all_timelines = self.client.statuses.home_timeline.get(page=page).statuses
        self.get_timeline(all_timelines, self.all_timeline)
        self.all_timeline_page = page

    def get_my_timeline(self, page=1):
        my_timelines = self.client.statuses.user_timeline.get(page=page).statuses
        self.get_timeline(my_timelines, self.my_timeline)
        self.my_timeline_page = page

    def get_mentions_timeline(self, page=1):
        mentions_timelines = self.client.statuses.mentions.get(page=page).statuses
        self.get_timeline(mentions_timelines, self.mentions)
        self.mentions_page = page

    def get_comment_to_me(self, page=1):
        comments_to_me = self.client.comments.to_me.get(page=page).comments
        self.get_timeline(comments_to_me, self.comment_to_me)
        self.comment_to_me_page = page

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

        wecase_new = NewpostWindow(action="reply", id=int(idstr))
        wecase_new.client = self.client
        wecase_new.exec_()

    def repost(self):
        listView = self.get_current_listView()
        model = self.get_current_model()

        row = listView.currentIndex().row()
        idstr = model.item(row, 1).text()

        wecase_new = NewpostWindow(action="retweet", id=int(idstr))
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
        idstr = self.comment_to_me.item(row, 2).text()
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

    def __init__(self, parent=None, action="new", id=None, cid=None):
        QtGui.QWidget.__init__(self, parent)
        self.action = action
        self.id = id
        self.cid = cid
        self.setupUi(self)
        self.setupSignals()

    def setupMyUi(self):
        if self.action == "new":
            self.pushButton_send.clicked.connect(self.send_tweet)

    def setupSignals(self):
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_picture.clicked.connect(self.add_image)
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
        self.client.statuses.repost.post(id=int(self.id), status=text)
        self.close()

    def comment(self):
        text = unicode(self.textEdit.toPlainText())
        self.client.comments.create.post(id=int(self.id), comment=text)
        self.close()

    def reply(self):
        text = unicode(self.textEdit.toPlainText())
        self.client.comments.reply.post(id=int(self.id), cid=int(self.cid), comment=text)
        self.close()

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

class HTMLDelegate(QtGui.QStyledItemDelegate):
    def paint(self, painter, option, index):
        options = QtGui.QStyleOptionViewItemV4(option)
        self.initStyleOption(options, index)
        options.text = options.text.replace(" ", "&nbsp;")

        style = QtGui.QApplication.style() if options.widget is None else options.widget.style()

        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(option.rect.width())

        options.text = ""
        style.drawControl(QtGui.QStyle.CE_ItemViewItem, options, painter);

        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()

        # Highlighting text if item is selected
        #if (optionV4.state & QStyle::State_Selected)
            #ctx.palette.setColor(QPalette::Text, optionV4.palette.color(QPalette::Active, QPalette::HighlightedText));

        textRect = style.subElementRect(QtGui.QStyle.SE_ItemViewItemText, options)
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        options = QtGui.QStyleOptionViewItemV4(option)
        self.initStyleOption(options,index)

        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        return QtCore.QSize(doc.idealWidth(), (doc.size().height()))


if __name__ == "__main__":
    try:
        os.mkdir(config_path.replace("/config_db", ""))
    except OSError:
        pass

    app = QtGui.QApplication(sys.argv)

    wecase_login = LoginWindow()
    wecase_main = WeCaseWindow()
    wecase_settings = WeSettingsWindow()

    wecase_login.show()
    sys.exit(app.exec_())
