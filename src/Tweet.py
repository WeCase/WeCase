#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented Model and Item for tweets
# Copyright: GPL v3 or later.

from PyQt4 import QtCore
from datetime import datetime
from WTimeParser import WTimeParser as time_parser


class TweetModel(QtCore.QAbstractListModel):
    def __init__(self, prototype, parent=None):
        super(TweetModel, self).__init__()
        self.setRoleNames(prototype.roles)
        self._tweets = []

    def appendRow(self, item):
        self.insertRow(self.rowCount(), item)

    def clear(self):
        self._tweets = []

    def data(self, index, role):
        return self._tweets[index.row()].data(role)

    def insertRow(self, row, item):
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self._tweets.insert(row, item)
        self.endInsertRows()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._tweets)


class UserItem(QtCore.QObject):
    def __init__(self, item, parent=None):
        super(UserItem, self).__init__()
        self._data = item

    @QtCore.pyqtProperty(str, constant=True)
    def id(self):
        return self._data.get('idstr')

    @QtCore.pyqtProperty(str, constant=True)
    def name(self):
        return self._data.get('name')

    @QtCore.pyqtProperty(str, constant=True)
    def avatar(self):
        return self._data.get('profile_image_url')


class TweetItem(QtCore.QObject):
    TWEET = 0
    RETWEET = 1
    COMMENT = 2
    roles = {
        QtCore.Qt.UserRole + 1: "type",
        QtCore.Qt.UserRole + 2: "id",
        QtCore.Qt.UserRole + 3: "author",
        QtCore.Qt.UserRole + 4: "time",
        QtCore.Qt.UserRole + 5: "text",
        QtCore.Qt.UserRole + 6: "original",
        QtCore.Qt.UserRole + 7: "thumbnail_pic",
        QtCore.Qt.UserRole + 8: "original_pic"
    }

    def __init__(self, item={}, parent=None):
        super(TweetItem, self).__init__()
        self._data = item

        if not item:
            return

        self._roleData = {
            "type": self.type,
            "id": self.id,
            "author": self.author,
            "time": self.time,
            "text": self.text,
            "original": self.original,
            "thumbnail_pic": self.thumbnail_pic,
            "original_pic": self.original_pic
        }

    def data(self, key):
        return self._roleData[self.roles[key]]

    @QtCore.pyqtProperty(int, constant=True)
    def type(self):
        if "retweeted_status" in self._data:
            return self.RETWEET
        elif "status" in self._data:
            return self.COMMENT
        else:
            return self.TWEET

    @QtCore.pyqtProperty(str, constant=True)
    def id(self):
        return self._data.get('idstr')

    @QtCore.pyqtProperty(QtCore.QObject, constant=True)
    def author(self):
        if "user" in self._data:
            self._user = UserItem(self._data.get('user'), self)
            return self._user
        else:
            return None

    @QtCore.pyqtProperty(str, constant=True)
    def time(self):
        return self._sinceTimeString(self._data.get('created_at'))

    @QtCore.pyqtProperty(str, constant=True)
    def text(self):
        return self._data.get('text')

    @QtCore.pyqtProperty(QtCore.QObject, constant=True)
    def original(self):
        if self.type == self.RETWEET:
            self._original = TweetItem(self._data.get('retweeted_status'))
            return self._original
        elif self.type == self.COMMENT:
            self._original = TweetItem(self._data.get('status'))
            return self._original
        else:
            return None

    @QtCore.pyqtProperty(str, constant=True)
    def thumbnail_pic(self):
        return self._data.get('thumbnail_pic', "")

    @QtCore.pyqtProperty(str, constant=True)
    def original_pic(self):
        return self._data.get('original_pic')

    def _sinceTimeString(self, createTime):
        if not createTime:
            return

        create = time_parser().parse(createTime)
        create_utc = (create - create.utcoffset()).replace(tzinfo=None)
        now_utc = datetime.utcnow()

        # Always compare UTC time, do NOT compare LOCAL time.
        # See http://coolshell.cn/articles/5075.html for more details.
        passedSeconds = (now_utc - create_utc).seconds

        # datetime do not support nagetive numbers
        if now_utc < create_utc:
            return self.tr("Time travel!")
        if passedSeconds < 60:
            return self.tr("%.0f seconds ago") % (passedSeconds)
        if passedSeconds < 3600:
            return self.tr("%.0f minutes ago") % (passedSeconds / 60)
        if passedSeconds < 86400:
            return self.tr("%.0f hours ago") % (passedSeconds / 3600)

        return self.tr("%.0f days ago") % (passedSeconds / 86400)
