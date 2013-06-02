#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented NewpostWindow.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import re
from copy import deepcopy
from WeHack import async
from PyQt4 import QtCore, QtGui
from weibo import APIError
from Tweet import TweetItem, TweetCommentModel
from Notify import Notify
from TweetUtils import tweetLength
from NewpostWindow_ui import Ui_NewPostWindow
from SmileyWindow import SmileyWindow
from TweetListWidget import TweetListWidget, SingleTweetWidget


class NewpostWindow(QtGui.QDialog, Ui_NewPostWindow):
    client = None
    image = None
    apiError = QtCore.pyqtSignal(str)
    sendSuccessful = QtCore.pyqtSignal()

    def __init__(self, client, action="new", tweet=None, parent=None):
        super(NewpostWindow, self).__init__(parent)
        self.client = client
        self.tweet = tweet
        self.action = action
        self.setupUi(self)
        self.textEdit.callback = self.mentions_suggest
        self.textEdit.mention_flag = "@"
        self.notify = Notify(timeout=1)

    def setupUi(self, widget):
        super(NewpostWindow, self).setupUi(widget)

        if self.action != "new":
            self.tweetWidget = SingleTweetWidget(self.client, self.tweet)
            self.tweetWidget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            self.verticalLayout.insertWidget(0, self.tweetWidget)
            self.verticalLayout.setStretch(0, 1)

            self.commentsModel = TweetCommentModel(
                                                   self.client.comments.show,
                                                   self)
            self.commentsModel.load(self.tweet.id)

            self.scrollArea = QtGui.QScrollArea()
            self.scrollArea.setWidgetResizable(True)
            self.commentsWidget = TweetListWidget(self.client)
            self.commentsWidget.setModel(self.commentsModel)
            self.scrollArea.setWidget(self.commentsWidget)
            self.verticalLayout.insertWidget(1, self.scrollArea)
            self.verticalLayout.setStretch(1, 1)


        self.checkChars()
        if self.action == "new":
            self.chk_repost.setEnabled(False)
            self.chk_comment.setEnabled(False)
            self.chk_comment_original.setEnabled(False)
        elif self.action == "retweet":
            self.chk_repost.setEnabled(False)
            self.pushButton_picture.setEnabled(False)
        elif self.action == "comment":
            self.chk_comment.setEnabled(False)
            self.pushButton_picture.setEnabled(False)
        elif self.action == "reply":
            self.chk_repost.setEnabled(False)
            self.chk_comment.setEnabled(False)
            self.pushButton_picture.setEnabled(False)

    def mentions_suggest(self, text):
        ret_users = []
        try:
            word = re.findall('@[-a-zA-Z0-9_\u4e00-\u9fa5]+', text)[-1]
            word = word.replace('@', '')
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
            self.new()
        elif self.action == "retweet":
            self.retweet()
        elif self.action == "comment":
            self.comment()
        elif self.action == "reply":
            self.reply()

    @async
    def retweet(self):
        text = str(self.textEdit.toPlainText())
        try:
            self.client.statuses.repost.post(id=int(self.tweet.id), status=text,
                                             is_comment=int((self.chk_comment.isChecked() +
                                             self.chk_comment_original.isChecked() * 2)))
            self.notify.showMessage(self.tr("WeCase"),
                                    self.tr("Retweet Success!"))
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

    @async
    def comment(self):
        text = str(self.textEdit.toPlainText())
        try:
            self.client.comments.create.post(id=int(self.tweet.id), comment=text,
                                             comment_ori=int(self.chk_comment_original.isChecked()))
            if self.chk_repost.isChecked():
                self.client.statuses.repost.post(id=int(self.tweet.id), status=text)
            self.notify.showMessage(self.tr("WeCase"),
                                    self.tr("Comment Success!"))
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

    @async
    def reply(self):
        text = str(self.textEdit.toPlainText())
        try:
            self.client.comments.reply.post(id=int(self.tweet.original.id), cid=int(self.tweet.id),
                                            comment=text,
                                            comment_ori=int(self.chk_comment_original.isChecked()))
            if self.chk_repost.isChecked():
                self.client.statuses.repost.post(id=int(self.tweet.id), status=text)
            self.notify.showMessage(self.tr("WeCase"),
                                    self.tr("Reply Success!"))
            self.sendSuccessful.emit()
        except APIError as e:
            self.apiError.emit(str(e))
            return

    @async
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
            # user may cancel the dialog, so check again
            if self.image:
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
