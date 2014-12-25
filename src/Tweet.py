# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented Model and Item for tweets
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore
from datetime import datetime
from TweetUtils import get_mid
from WTimeParser import WTimeParser as time_parser
from WeHack import async, UNUSED
from TweetUtils import tweetLength
from rpweibo import APIError
import re
import const


class WEvent():

    def __init__(self):
        self._callbacks = []

    def connect(self, func):
        self._callbacks.append(func)

    def disconnect(self, func):
        self._callbacks.remove(func)

    def emit(self, *args, **kwargs):
        for func in self._callbacks:
            try:
                func(*args, **kwargs)
            except TypeError:
                func.emit(*args, **kwargs)


class WListModel():

    def __init__(self):
        self._items = []
        self._tweets = self._items
        self.rowsInserted = WEvent()

    def _append(self, items):
        orig_len = len(self)
        self._items.extend(items)
        self.rowsInserted.emit(None, orig_len, orig_len + len(items) - 1)

    def _insert(self, idx, items):
        if idx == len(self) or idx == -1:
            self._append(items)
            return

        counter = idx
        for i in items:
            self._items.insert(counter, i)
            counter += 1
        self.rowsInserted.emit(None, idx, idx + len(items) - 1)

    def clear(self):
        self._items.clear()

    def __getitem__(self, idx):
        return self._items[idx]

    def __len__(self):
        return len(self._items)

    def appendRows(self, items):
        self._append(items)

    def insertRows(self, row, items):
        self._insert(row, items)


class TweetSimpleModel(WListModel):

    def __init__(self, parent=None):
        super().__init__()

    def appendRows(self, items):
        super().appendRows([TweetItem(item) for item in items])

    def insertRows(self, row, items):
        super().insertRows(row, [TweetItem(item) for item in items])


class TweetTimelineBaseModel(TweetSimpleModel):

    def __init__(self, timeline=None, parent=None):
        super(TweetTimelineBaseModel, self).__init__(parent)
        self.timeline = timeline
        self.lock = False
        self._nomore = False

        self.timelineLoaded = WEvent()
        self.nothingLoaded = WEvent()
        self.apiException = WEvent()

    def timeline_get(self):
        raise NotImplementedError

    def timeline_new(self):
        raise NotImplementedError

    def timeline_old(self):
        raise NotImplementedError

    def first_id(self):
        assert self._tweets
        return int(self._tweets[0].id)

    def last_id(self):
        assert self._tweets
        return int(self._tweets[-1].id)

    @async
    def _common_get(self, timeline_func, pos):
        if self.lock:
            return
        self.lock = True

        # timeline is just a pointer to the method.
        # We are in another thread now, call it. UI won't freeze.
        try:
            timeline = timeline_func()
        except APIError as e:
            timeline = []
            self.apiException.emit(e)

        if not timeline:
            if pos == -1:
                self._nomore = True
            self.nothingLoaded.emit(pos)

        if pos == -1:
            self.appendRows(timeline)
        else:
            self.insertRows(0, timeline)

        self.lock = False

    def load(self):
        self.page = 1
        timeline = self.timeline_get
        self._common_get(timeline, -1)

    def new(self):
        if self._tweets:
            timeline = self.timeline_new
            self._common_get(timeline, 0)
            self.timelineLoaded.emit()
        else:
            self.load()

    def next(self):
        if self._nomore:
            self.nothingLoaded.emit(-1)
        elif self._tweets:
            timeline = self.timeline_old
            self._common_get(timeline, -1)
        else:
            self.load()


class TweetCommonModel(TweetTimelineBaseModel):

    def __init__(self, timeline=None, parent=None):
        super(TweetCommonModel, self).__init__(timeline, parent)

    def timeline_get(self, page=1):
        timeline = self.timeline.get(page=page).statuses
        return timeline

    def timeline_new(self):
        timeline = self.timeline.get(since_id=self.first_id()).statuses
        return timeline

    def timeline_old(self):
        timeline = self.timeline.get(max_id=self.last_id()).statuses
        timeline = timeline[1::]
        return timeline


class TweetUserModel(TweetTimelineBaseModel):

    def __init__(self, timeline, uid, parent=None):
        super(TweetUserModel, self).__init__(timeline, parent)
        self._uid = uid

    def timeline_get(self, page=1):
        timeline = self.timeline.get(page=page, uid=self._uid).statuses
        return timeline

    def timeline_new(self):
        timeline = self.timeline.get(since_id=self.first_id(),
                                     uid=self._uid).statuses
        return timeline

    def timeline_old(self):
        timeline = self.timeline.get(max_id=self.last_id(), uid=self._uid).statuses
        timeline = timeline[1::]
        return timeline

    def uid(self):
        return self._uid


class TweetCommentModel(TweetTimelineBaseModel):

    def __init__(self, timeline=None, parent=None):
        super(TweetCommentModel, self).__init__(timeline, parent)
        self.page = 0

    def timeline_get(self, page=1):
        timeline = self.timeline.get(page=page).comments
        return timeline

    def timeline_new(self):
        timeline = self.timeline.get(since_id=self.first_id()).comments
        return timeline

    def timeline_old(self):
        timeline = self.timeline.get(max_id=self.last_id()).comments
        timeline = timeline[1::]
        return timeline


class TweetUnderCommentModel(TweetTimelineBaseModel):
    def __init__(self, timeline=None, id=0, parent=None):
        super(TweetUnderCommentModel, self).__init__(timeline, parent)
        self.id = id

    def timeline_get(self, page=1):
        timeline = self.timeline.get(id=self.id, page=page).comments
        return timeline

    def timeline_new(self):
        timeline = self.timeline.get(id=self.id, since_id=self.first_id()).comments
        return timeline

    def timeline_old(self):
        timeline = self.timeline.get(id=self.id, max_id=self.last_id()).comments
        timeline = timeline[1::]
        return timeline


class TweetRetweetModel(TweetTimelineBaseModel):
    def __init__(self, timeline=None, id=0, parent=None):
        super(TweetRetweetModel, self).__init__(timeline, parent)
        self.id = id

    def timeline_get(self, page=1):
        try:
            timeline = self.timeline.get(id=self.id, page=page).reposts
        except AttributeError:
            # Issue 115: So the censorship, fuck you!
            timeline = []
        return timeline

    def timeline_new(self):
        timeline = self.timeline.get(id=self.id, since_id=self.first_id()).reposts
        return timeline

    def timeline_old(self):
        timeline = self.timeline.get(id=self.id, max_id=self.last_id()).reposts
        timeline = timeline[1::]
        return timeline


class TweetTopicModel(TweetTimelineBaseModel):

    def __init__(self, timeline, topic, parent=None):
        super(TweetTopicModel, self).__init__(timeline, parent)
        self._topic = topic.replace("#", "")
        self.page = 1

    def timeline_get(self):
        timeline = self.timeline.get(q=self._topic, page=self.page).statuses
        return timeline

    def timeline_new(self):
        timeline = self.timeline.get(q=self._topic, page=1).statuses
        for tweet in timeline:
            if TweetItem(tweet).id == self.first_id():
                return list(timeline[:timeline.index(tweet)])
        return timeline

    def timeline_old(self):
        self.page += 1
        return self.timeline_get()

    def topic(self):
        return self._topic


class TweetFilterModel(WListModel):

    def __init__(self, parent=None):
        super().__init__()
        self._model = None
        self._appearInfo = {}
        self._userInfo = {}
        self._wordWarKeywords = []
        self._blockWordwars = False
        self._maxTweetsPerUser = -1
        self._maxRetweets = -1
        self._keywordsAsRegexs = False
        self._tweetKeywordBlacklist = []
        self._usersBlackList = []
        self.timelineLoaded = WEvent()
        self.nothingLoaded = WEvent()

    def model(self):
        return self._model

    def setModel(self, model):
        self._model = model
        self._model.timelineLoaded.connect(self.timelineLoaded)
        self._model.nothingLoaded.connect(self.nothingLoaded)
        self._model.rowsInserted.connect(self._rowsInserted)

    def setKeywordsAsRegexs(self, state):
        self._keywordsAsRegexs = bool(state)

    def setTweetsKeywordsBlacklist(self, blacklist):
        self._tweetKeywordBlacklist = blacklist

    def setWordWarKeywords(self, blacklist):
        self._wordWarKeywords = blacklist

    def setUsersBlacklist(self, blacklist):
        self._usersBlackList = blacklist

    def setBlockWordwars(self, state):
        self._blockWordwars = bool(state)

    def setMaxTweetsPerUser(self, max):
        self._maxTweetsPerUser = max

    def setMaxRetweets(self, max):
        self._maxRetweets = max

    def _inBlacklist(self, tweet):
        if not tweet:
            return False
        elif self._inBlacklist(tweet.original):
            return True

        # Put all your statements at here
        if tweet.withKeywords(self._tweetKeywordBlacklist, self._keywordsAsRegexs):
            return True
        if tweet.author and (tweet.author.name in self._usersBlackList):
            return True
        return False

    def maxTweetsPerUserFilter(self, items):
        new_items = []

        for item in items:
            if item.author.id not in self._userInfo:
                self._userInfo[item.author.id] = 0

            if self._userInfo[item.author.id] > self._maxTweetsPerUser:
                continue
            else:
                self._userInfo[item.author.id] += 1
                new_items.append(item)

        return new_items

    def maxRetweetsFilter(self, items):
        new_items = []

        for item in items:
            if not item.original:
                continue

            if item.original.id not in self._appearInfo:
                self._appearInfo[item.original.id] = {"count": 0, "wordWarKeywords": 0}

            if self._appearInfo[item.original.id]["count"] > self._maxRetweets:
                continue
            else:
                self._appearInfo[item.original.id]["count"] += 1
                new_items.append(item)

        return new_items

    def wordWarFilter(self, items):
        # If a same tweet retweeted more than 3 times, and
        # there are three retweets include insulting keywords,
        # then it is a word-war-tweet. Block it and it's retweets.
        new_items = []

        for item in items:
            if not item.original:
                continue

            if item.original.id not in self._appearInfo:
                self._appearInfo[item.original.id] = {"count": 0, "wordWarKeywords": 0}
            info = self._appearInfo[item.original.id]
            info["count"] += 1
            if item.withKeywords(self._wordWarKeywords, self._keywordsAsRegexs):
                info["wordWarKeywords"] += 1
            self._appearInfo[item.original.id] = info

        for item in items:
            if item.original:
                id = item.original.id
            else:
                id = item.id

            try:
                info = self._appearInfo[id]
            except KeyError:
                new_items.append(item)
                continue

            if info["count"] >= 3 and info["wordWarKeywords"] >= 3:
                continue
            else:
                new_items.append(item)

        return new_items

    def filter(self, items):
        new_items = []
        for item in items:
            if self._inBlacklist(item):
                continue
            else:
                new_items.append(item)

        if self._blockWordwars:
            new_items = self.wordWarFilter(new_items)
        if self._maxRetweets != -1:
            new_items = self.maxRetweetsFilter(new_items)
        if self._maxTweetsPerUser != -1:
            new_items = self.maxTweetsPerUserFilter(new_items)

        return new_items

    def _rowsInserted(self, parent, start, end):
        tweets = []
        for index in range(start, end + 1):
            item = self._model[index]
            tweets.insert(index, item)

        filteredTweets = self.filter(tweets)
        while start != 0 and tweets and not filteredTweets:
            self._model.next()
            return

        if len(filteredTweets) == 0:
            return

        self.insertRows(start, filteredTweets)

    def __getattr__(self, attr):
        return eval("self._model.%s" % attr)


class UserItem():
    def __init__(self, item, parent=None):
        UNUSED(parent)
        # HACK: Ignore parent, can't create a child with different thread.
        # Where is the thread? I don't know...
        super(UserItem, self).__init__()
        self._data = item
        self.client = const.client

        if self._data.get('id') and self._data.get('name'):
            return
        else:
            self._loadCompleteInfo()

    def _loadCompleteInfo(self):
        if self._data.get('id'):
            self._data = self.client.api("users/show").get(uid=self._data.get('id'))
        elif self._data.get('name'):
            self._data = self.client.api("users/show").get(screen_name=self._data.get('name'))

    @property
    def id(self):
        return self._data.get('id')

    @property
    def name(self):
        return self._data.get('name')

    @property
    def avatar(self):
        return self._data.get('profile_image_url')

    @property
    def verify_type(self):
        typ = self._data.get("verified_type")
        if typ == 0:
            return "personal"
        elif typ in [1, 2, 3, 4, 5, 6, 7]:
            return "organization"
        else:
            return None

    @property
    def verify_reason(self):
        return self._data.get("verified_reason")


class TweetItem():
    TWEET = 0
    RETWEET = 1
    COMMENT = 2

    def __init__(self, data={}, parent=None):
        super(TweetItem, self).__init__()
        self._data = data
        self.client = const.client
        self.__isFavorite = False

    @property
    def type(self):
        if "retweeted_status" in self._data:
            return self.RETWEET
        elif "status" in self._data:
            return self.COMMENT
        else:
            return self.TWEET

    @property
    def id(self):
        return self._data.get('id')

    @property
    def mid(self):
        decimal_mid = str(self._data.get('mid'))
        encode_mid = get_mid(decimal_mid)
        return encode_mid

    @property
    def url(self):
        try:
            uid = self._data['user']['id']
            mid = get_mid(self._data['mid'])
        except KeyError:
            # Sometimes Sina's API doesn't return user
            # when our tweet is deeply nested. Just forgot it.
            return ""
        return 'http://weibo.com/%s/%s' % (uid, mid)

    @property
    def author(self):
        if "user" in self._data:
            self._user = UserItem(self._data.get('user'), self)
            return self._user
        else:
            return None

    @property
    def timestamp(self):
        return self._data.get('created_at')

    @property
    def text(self):
        return self._data.get('text')

    @property
    def original(self):
        try:
            return self._original
        except AttributeError:
            pass

        if self.type == self.RETWEET:
            self._original = TweetItem(self._data.get('retweeted_status'))
            return self._original
        elif self.type == self.COMMENT:
            self._original = TweetItem(self._data.get('status'))
            return self._original
        else:
            return None

    @property
    def thumbnail_pic(self):
        # Checkout Issue #101.
        results = []

        pic_urls = self._data.get("pic_urls")
        if pic_urls:
            for url in pic_urls:
                results.append(url['thumbnail_pic'])
            return results

        pic_ids = self._data.get("pic_ids")
        if pic_ids:
            for id in pic_ids:
                results.append("http://ww1.sinaimg.cn/thumbnail/%s" % id)
            return results

        pic_fallback = self._data.get("thumbnail_pic")
        if pic_fallback:
            results.append(results)
            return results

        return None

    @property
    def original_pic(self):
        return self._data.get('original_pic')

    @property
    def source(self):
        return self._data.get('source')

    @property
    def retweets_count(self):
        return self._data.get('reposts_count', 0)

    @property
    def comments_count(self):
        return self._data.get('comments_count', 0)

    @property
    def passedSeconds(self):
        create = time_parser().parse(self.timestamp)
        create_utc = (create - create.utcoffset()).replace(tzinfo=None)
        now_utc = datetime.utcnow()

        # Always compare UTC time, do NOT compare LOCAL time.
        # See http://coolshell.cn/articles/5075.html for more details.
        if now_utc < create_utc:
            # datetime do not support negative numbers
            return -1
        else:
            passedSeconds = (now_utc - create_utc).total_seconds()
            return passedSeconds

    def isFavorite(self):
        return self.__isFavorite

    def _cut_off(self, text):
        cut_text = ""
        for char in text:
            if tweetLength(cut_text) >= 140:
                break
            else:
                cut_text += char
        return cut_text

    def append_existing_replies(self, text=""):
        if self.original.original:
            text += "//@%s:%s//@%s:%s" % (
                    self.author.name, self.text,
                    self.original.author.name, self.original.text)
        else:
            text += "//@%s:%s" % (self.author.name, self.text)
        return text

    def reply(self, text, comment_ori=False, retweet=False):
        self.client.api("comments/reply").post(id=self.original.id, cid=self.id,
                                               comment=text, comment_ori=int(comment_ori))
        if retweet:
            text = self.append_existing_replies(text)
            text = self._cut_off(text)
            self.original.retweet(text)

    def retweet(self, text, comment=False, comment_ori=False):
        self.client.api("statuses/repost").post(id=self.id, status=text,
                                                is_comment=int(comment + comment_ori * 2))

    def comment(self, text, comment_ori=False, retweet=False):
        self.client.api("comments/create").post(id=self.id, comment=text,
                                                comment_ori=int(comment_ori))
        if retweet:
            self.retweet(text)

    def delete(self):
        if self.type in [self.TWEET, self.RETWEET]:
            self.client.api("statuses/destroy").post(id=self.id)
        elif self.type == self.COMMENT:
            self.client.api("comments/destroy").post(cid=self.id)

    def setFavorite(self, state):
        if self.type not in [self.TWEET, self.RETWEET]:
            raise TypeError

        if state:
            assert(not self.__isFavorite)
            self.client.api("favorites/create").post(id=self.id)
            self.__isFavorite = True
        else:
            assert(self.__isFavorite)
            self.client.api("favorites/destroy").post(id=self.id)
            self.__isFavorite = False

    def setFavoriteForce(self, state):
        self.__isFavorite = bool(state)

    def refresh(self):
        if self.type in [self.TWEET, self.RETWEET]:
            self._data = self.client.api("statuses/show").get(id=self.id)

    def _withKeyword(self, keyword):
        if keyword in self.text:
            return True
        else:
            return False

    def _withKeywords(self, keywords):
        for keyword in keywords:
            if self._withKeyword(keyword):
                return True
        return False

    def _withRegex(self, pattern):
        try:
            result = re.match(pattern, self.text)
        except (ValueError, TypeError):
            return False

        if result:
            return True
        else:
            return False

    def _withRegexs(self, patterns):
        for pattern in patterns:
            if self._withRegex(pattern):
                return True
        return False

    def withKeyword(self, pattern, regex=False):
        if regex:
            return self._withRegex(pattern)
        else:
            return self._withKeyword(pattern)

    def withKeywords(self, patterns, regex=False):
        if regex:
            return self._withRegexs(patterns)
        else:
            return self._withKeywords(patterns)
