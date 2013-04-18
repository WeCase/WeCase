#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented Model and Item for tweets
# Copyright: GPL v3 or later.

from PyQt4 import QtCore
from datetime import datetime
from WTimeParser import WTimeParser as time_parser


class TweetModel(QtCore.QAbstractListModel):
    def __init__(self, prototype, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.setRoleNames(prototype.roles)
        self.tweets = []

    def appendRow(self, item):
        self.insertRow(self.rowCount(), item)

    def clear(self):
        del self.tweets
        self.tweets = []

    def data(self, index, role):
        return self.tweets[index.row()].data(role)

    def insertRow(self, row, item):
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.tweets.insert(row, item)
        self.endInsertRows()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.tweets)


class TweetItem(QtCore.QAbstractItemModel):
    roles = {
        QtCore.Qt.UserRole + 1: "type",
        QtCore.Qt.UserRole + 2: "id",
        QtCore.Qt.UserRole + 3: "author",
        QtCore.Qt.UserRole + 4: "avatar",
        QtCore.Qt.UserRole + 5: "content",
        QtCore.Qt.UserRole + 6: "time",
        QtCore.Qt.UserRole + 7: "original_id",
        QtCore.Qt.UserRole + 8: "original_content",
        QtCore.Qt.UserRole + 9: "original_author",
        QtCore.Qt.UserRole + 10: "original_time",
        QtCore.Qt.UserRole + 11: "thumbnail_pic"
    }

    def __init__(self, type="", id="", author="", avatar="", content="",
                 time="", original_id="", original_content="",
                 original_author="", original_time="", thumbnail_pic="",
                 parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)

        self._data = {
            "type": type,
            "id": id,
            "author": author,
            "avatar": avatar,
            "content": content,
            "time": self.sinceTimeString(time),
            "original_id": original_id,
            "original_content": original_content,
            "original_author": original_author,
            "original_time": original_time,
            "thumbnail_pic": thumbnail_pic
        }

    def sinceTimeString(self, createTime):
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

    def data(self, role):
        return self._data[self.roles[role]]
