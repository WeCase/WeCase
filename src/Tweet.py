#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented Model and Item for tweets
# Copyright: GPL v3 or later.

# TODO: Refactoring Needed! But I don't have time... I think I'll do it soon.

import threading
from PyQt4 import QtCore
from datetime import datetime
from TweetUtils import get_mid
from WTimeParser import WTimeParser as time_parser
from WeHack import async


class TweetSimpleModel(QtCore.QAbstractListModel):
    rowInserted = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(TweetSimpleModel, self).__init__()
        self._tweets = []

    def appendRow(self, item):
        self.insertRow(self.rowCount(), item)

    def appendRows(self, items):
        for item in items:
            self.appendRow(TweetItem(item))

    def clear(self):
        self._tweets = []

    def data(self, index, role):
        return self._tweets[index.row()].data(role)

    def get_item(self, row):
        return self._tweets[row]

    def insertRow(self, row, item):
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self._tweets.insert(row, item)
        self.rowInserted.emit(row)
        self.endInsertRows()

    def insertRows(self, row, items):
        self.beginInsertRows(QtCore.QModelIndex(), row, row + len(items) - 1)
        for item in items:
            self._tweets.insert(row, TweetItem(item))
            self.rowInserted.emit(row)
        self.endInsertRows()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._tweets)


class TweetTimelineBaseModel(TweetSimpleModel):

    timelineLoaded = QtCore.pyqtSignal()

    def __init__(self, timeline=None, parent=None):
        super(TweetTimelineBaseModel, self).__init__(parent)
        self.timeline = timeline
        self.lock = False

    def timeline_get(self):
        raise NotImplementedError

    def timeline_new(self):
        raise NotImplementedError

    def timeline_old(self):
        raise NotImplementedError

    def first_id(self):
        return int(self._tweets[0].id)

    def last_id(self):
        return int(self._tweets[-1].id)

    @async
    def _common_get(self, timeline, pos):
        if self.lock:
            return
        self.lock = True
        # timeline is just a pointer to the method.
        # We are in another thread now, call it. UI won't freeze.
        timeline = timeline()
        if pos == -1:
            self.appendRows(timeline)
        else:
            self.insertRows(pos, timeline)
        self.lock = False

    def load(self):
        timeline = self.timeline_get
        self._common_get(timeline, -1)

    def new(self):
        timeline = self.timeline_new
        self._common_get(timeline, 0)
        self.timelineLoaded.emit()

    def next(self):
        timeline = self.timeline_old
        self._common_get(timeline, -1)


class TweetCommonModel(TweetTimelineBaseModel):

    def __init__(self, timeline=None, parent=None):
        super(TweetCommonModel, self).__init__(timeline, parent)

    def timeline_get(self):
        timeline = self.timeline.get(page=1).statuses
        return timeline

    def timeline_new(self):
        timeline = self.timeline.get(since_id=self.first_id()).statuses[::-1]
        return timeline

    def timeline_old(self):
        timeline = self.timeline.get(max_id=self.last_id()).statuses
        timeline = timeline[1::]
        return timeline


class TweetCommentModel(TweetTimelineBaseModel):
    def __init__(self, timeline=None, parent=None):
        super(TweetCommentModel, self).__init__(timeline, parent)
        self.page = 0

    def timeline_get(self):
        self.page += 1
        timeline = self.timeline.get(page=self.page).comments
        return timeline

    def timeline_new(self):
        timeline = self.timeline.get(since_id=self.first_id()).comments[::-1]
        return timeline

    def timeline_old(self):
        timeline = self.timeline.get(max_id=self.last_id()).statuses
        return timeline


class TweetUnderCommentModel(TweetTimelineBaseModel):
    def __init__(self, timeline=None, id=0, parent=None):
        super(TweetUnderCommentModel, self).__init__(timeline, parent)
        self.id = id
        self.page = 0

    def timeline_get(self):
        self.page += 1
        timeline = self.timeline.get(id=self.id, page=self.page).comments
        return timeline

    def timeline_new(self):
        timeline = self.timeline.get(id=id, since_id=self.first_id()).comments[::-1]
        return timeline

    def timeline_old(self):
        timeline = self.timeline.get(id=id, max_id=self.last_id()).comments
        return timeline


class TweetRetweetModel(TweetTimelineBaseModel):
    def __init__(self, timeline=None, id=0, parent=None):
        super(TweetRetweetModel, self).__init__(timeline, parent)
        self.id = id
        self.page = 0

    def timeline_get(self):
        self.page += 1
        timeline = self.timeline.get(id=self.id, page=self.page).reposts
        return timeline

    def timeline_new(self):
        timeline = self.timeline.get(id=self.id, since_id=self.first_id).reposts[::-1]
        return timeline

    def timeline_old(self):
        timeline = self.timeline.get(id=self.id, max_id=self.last_id).reposts
        return timeline


class UserItem(QtCore.QObject):
    def __init__(self, item, parent=None):
        super(UserItem, self).__init__()
        self._data = item

    @QtCore.pyqtProperty(int, constant=True)
    def id(self):
        return self._data.get('id')

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

    def __init__(self, item={}, parent=None):
        super(TweetItem, self).__init__()
        self._data = item

        if not item:
            return

    @QtCore.pyqtProperty(int, constant=True)
    def type(self):
        if "retweeted_status" in self._data:
            return self.RETWEET
        elif "status" in self._data:
            return self.COMMENT
        else:
            return self.TWEET

    @QtCore.pyqtProperty(int, constant=True)
    def id(self):
        return self._data.get('id')

    @QtCore.pyqtProperty(str, constant=True)
    def mid(self):
        decimal_mid = str(self._data.get('mid'))
        encode_mid = get_mid(decimal_mid)
        return encode_mid

    @QtCore.pyqtProperty(str, constant=True)
    def url(self):
        try:
            uid = self._data['user']['id']
            mid = get_mid(self._data['mid'])
        except KeyError:
            # Sometimes Sina's API doesn't return user
            # when our tweet is deeply nested. Just forgot it.
            return ""
        return 'http://weibo.com/%s/%s' % (uid, mid)

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

    @QtCore.pyqtProperty(int, constant=True)
    def retweets_count(self):
        return str(self._data.get('reposts_count', 0))

    @QtCore.pyqtProperty(int, constant=True)
    def comments_count(self):
        return str(self._data.get('comments_count', 0))

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
            return self.tr("Future!")
        if passedSeconds < 60:
            return self.tr("%.0fs ago") % (passedSeconds)
        if passedSeconds < 3600:
            return self.tr("%.0fm ago") % (passedSeconds / 60)
        if passedSeconds < 86400:
            return self.tr("%.0fh ago") % (passedSeconds / 3600)

        return self.tr("%.0fd ago") % (passedSeconds / 86400)
