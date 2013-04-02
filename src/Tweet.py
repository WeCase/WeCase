#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented Model and Item for tweets
# Copyright: GPL v3 or later.

from PyQt4 import QtCore
from datetime import datetime
from dateutil import parser as time_parser


class TweetModel(QtCore.QAbstractListModel):
    def __init__(self, prototype, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.setRoleNames(prototype.roleNames())
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
    typeRole = QtCore.Qt.UserRole + 1
    idRole = QtCore.Qt.UserRole + 2
    authorRole = QtCore.Qt.UserRole + 3
    avatarRole = QtCore.Qt.UserRole + 4
    contentRole = QtCore.Qt.UserRole + 5
    timeRole = QtCore.Qt.UserRole + 6
    originalIdRole = QtCore.Qt.UserRole + 7
    originalContentRole = QtCore.Qt.UserRole + 8
    originalAuthorRole = QtCore.Qt.UserRole + 9
    originalTimeRole = QtCore.Qt.UserRole + 10
    thumbnailPicRole = QtCore.Qt.UserRole + 11

    def __init__(self, type="", id="", author="", avatar="", content="",
                 time="", original_id="", original_content="",
                 original_author="", original_time="", thumbnail_pic="",
                 parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)

        self.type = type
        self.id = id
        self.author = author
        self.avatar = avatar
        self.content = content
        self.time = time
        self.original_id = original_id
        self.original_content = original_content
        self.original_author = original_author
        self.original_time = original_time
        self.thumbnail_pic = thumbnail_pic

    def sinceTimeString(self, createTime):
        create = time_parser.parse(createTime)
        create_utc = (create - create.utcoffset()).replace(tzinfo=None)
        now_utc = datetime.utcnow()

        # Always compare UTC time, do NOT compare LOCAL time.
        # See http://coolshell.cn/articles/5075.html for more details.
        passedSeconds = (now_utc - create_utc).seconds

        # datetime do not support nagetive numbers
        if now_utc < create_utc:
            return "Time travel!"
        if passedSeconds < 60:
            return "%.0f seconds ago" % (passedSeconds)
        if passedSeconds < 3600:
            return "%.0f minutes ago" % (passedSeconds / 60)
        if passedSeconds < 86400:
            return "%.0f hours ago" % (passedSeconds / 3600)

        return "%.0f days ago" % (passedSeconds / 86400)

    def roleNames(self):
        names = {}
        names[self.typeRole] = "type"
        names[self.idRole] = "id"
        names[self.authorRole] = "author"
        names[self.avatarRole] = "avatar"
        names[self.contentRole] = "content"
        names[self.timeRole] = "time"
        names[self.originalIdRole] = "original_id"
        names[self.originalContentRole] = "original_content"
        names[self.originalAuthorRole] = "original_author"
        names[self.originalTimeRole] = "original_time"
        names[self.thumbnailPicRole] = "thumbnail_pic"
        return names

    def data(self, role):
        if role == self.typeRole:
            return self.type
        elif role == self.idRole:
            return self.id
        elif role == self.authorRole:
            return self.author
        elif role == self.avatarRole:
            return self.avatar
        elif role == self.contentRole:
            return self.content
        elif role == self.timeRole:
            return self.sinceTimeString(self.time)
        elif role == self.originalIdRole:
            return self.original_id
        elif role == self.originalContentRole:
            return self.original_content
        elif role == self.originalAuthorRole:
            return self.original_author
        elif role == self.originalTimeRole:
            return self.original_time
        elif role == self.thumbnailPicRole:
            return self.thumbnail_pic
        else:
            return None
