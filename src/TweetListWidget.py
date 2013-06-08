import os
import re
import urllib.request
from time import sleep
from WeHack import async
from PyQt4 import QtCore, QtGui
from Tweet import TweetItem
from WIconLabel import WIconLabel
from WTweetLabel import WTweetLabel
from WAsyncLabel import WAsyncLabel
from WTimer import WTimer
import const
from const import cache_path


class TweetListWidget(QtGui.QWidget):

    def __init__(self, parent=None, without=[]):
        super(TweetListWidget, self).__init__(parent)
        self.tweetListWidget = SimpleTweetListWidget(None, without)
        self.setupUi()

    def setupUi(self):
        self.layout = QtGui.QVBoxLayout()
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.tweetListWidget)
        self.layout.addWidget(self.scrollArea)
        self.layout.setMargin(0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.loadMore)

    def setModel(self, model):
        self.tweetListWidget.setModel(model)

    def loadMore(self, value):
       if value == self.scrollArea.verticalScrollBar().maximum():
            model = self.tweetListWidget.model
            model.next()

    def moveToTop(self):
        self.scrollArea.verticalScrollBar().setSliderPosition(0)


class SimpleTweetListWidget(QtGui.QWidget):

    def __init__(self, parent=None, without=[]):
        super(SimpleTweetListWidget, self).__init__(parent)
        self.client = const.client
        self.without = without
        self.setupUi()

    def setupUi(self):
        self.layout = QtGui.QVBoxLayout(self)
        self.setLayout(self.layout)

    def setModel(self, model):
        self.model = model
        self.model.rowsInserted.connect(self._rowsInserted)

    def _rowsInserted(self, parent, start, end):
        for index in range(start, end + 1):
            item = self.model.get_item(index)
            widget = SingleTweetWidget(item, self.without, self)
            self.layout.insertWidget(index, widget)


class SingleTweetWidget(QtGui.QFrame):

    imageLoaded = QtCore.pyqtSignal()
    commonSignal = QtCore.pyqtSignal(object)

    def __init__(self, tweet=None, without=[], parent=None):
        super(SingleTweetWidget, self).__init__(parent)
        self.commonSignal.connect(self.commonProcessor)
        self.tweet = tweet
        self.client = const.client
        self.without = without
        self.setObjectName("SingleTweetWidget")
        self.setupUi()
        self.download_lock = False

    def setupUi(self):
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        #self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.avatar = WAsyncLabel(self)
        self.avatar.setObjectName("avatar")
        self.avatar.setPixmap(self.tweet.author.avatar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.avatar.sizePolicy().hasHeightForWidth())
        self.avatar.setSizePolicy(sizePolicy)
        self.avatar.setAlignment(QtCore.Qt.AlignTop)
        self.verticalLayout_2.addWidget(self.avatar)

        self.time = QtGui.QLabel(self)
        self.time.setObjectName("time")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time.sizePolicy().hasHeightForWidth())
        self.time.setSizePolicy(sizePolicy)
        self.time.setOpenExternalLinks(True)
        self.verticalLayout_2.addWidget(self.time)
        self.verticalLayout_2.setAlignment(QtCore.Qt.AlignTop)

        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.username = QtGui.QLabel(self)
        self.username.setObjectName("username")
        self.username.setAlignment(QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.username)

        self.tweetText = WTweetLabel(self)
        self.tweetText.setObjectName("tweetText")
        #self.tweetText.setWordWrap(True)
        self.tweetText.setAlignment(QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.tweetText)

        if self.tweet.thumbnail_pic and (not "image" in self.without):
            self.imageWidget = self._createImageLabel(self.tweet.thumbnail_pic)
            self.verticalLayout.addWidget(self.imageWidget)

        if self.tweet.original and (not "original" in self.without):
            self.originalLabel = self._createOriginalLabel()
            self.verticalLayout.addWidget(self.originalLabel)

        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 10)
        #self.verticalLayout.setStretch(1, 1)
        #self.verticalLayout.setStretch(2, 10)

        self.counterHorizontalLayout = QtGui.QHBoxLayout()
        self.counterHorizontalLayout.setObjectName("counterhorizontalLayout")
        self.horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                          QtGui.QSizePolicy.Minimum)
        self.counterHorizontalLayout.addItem(self.horizontalSpacer)
        if not (self.tweet.type == TweetItem.COMMENT):
            self.retweet = WIconLabel(self)
            self.retweet.setObjectName("retweet")
            self.retweet.setText(str(self.tweet.retweets_count))
            self.retweet.setIcon("./icon/retweets.png")
            self.retweet.clicked.connect(self._retweet)
            self.counterHorizontalLayout.addWidget(self.retweet)

            self.comment = WIconLabel(self)
            self.comment.setObjectName("comment")
            self.comment.setIcon("./icon/comments.png")
            self.comment.setText(str(self.tweet.comments_count))
            self.comment.clicked.connect(self._comment)
            self.counterHorizontalLayout.addWidget(self.comment)

            self.favorite = WIconLabel(self)
            self.favorite.setIcon("./icon/no_favorites.png")
            self.favorite.clicked.connect(self._favorite)
            self.counterHorizontalLayout.addWidget(self.favorite)

            self.counterHorizontalLayout.setAlignment(QtCore.Qt.AlignTop)
            #self.verticalLayout.setSpacing(0)
        elif self.tweet.type == TweetItem.COMMENT:
            self.reply = WIconLabel(self)
            self.reply.setObjectName("reply")
            self.reply.setIcon("./icon/retweets.png")
            self.reply.clicked.connect(self._reply)
            self.counterHorizontalLayout.addWidget(self.reply)

        self.verticalLayout.addLayout(self.counterHorizontalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)

        #self.verticalLayout.setStretch(3, 10)
        #self.verticalLayout.setStretch(4, 1)

        self.setStyleSheet("""
            QFrame#SingleTweetWidget {
                border-bottom: 2px solid palette(highlight);
                border-radius: 0px;
                padding: 2px;
            }
        """)

        self.username.setText(" " + self.tweet.author.name)
        self.tweetText.setText(self._create_html_url(self.tweet.text))
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_time)
        self._update_time()

    def _setup_timer(self):
        self.timer.stop()
        passedSeconds = self.tweet.passedSeconds
        if passedSeconds < 60:
            self.timer.start(1 * 1000)
        elif passedSeconds < 3600:
            self.timer.start(60 * 1000)
        elif passedSeconds < 86400:
            self.timer.start(60 * 60 * 1000)
        else:
            self.timer.start(60 * 60 * 24 * 1000)

    def _update_time(self):
        if self.tweet.type != TweetItem.COMMENT:
            self.time.setText("<a href='%s'>%s</a>" % (self.tweet.url, self.tweet.time))
        else:
            self.time.setText(self.tweet.time)
        self._setup_timer()

    def _createOriginalLabel(self):
        widget = QtGui.QWidget(self)
        widget.setObjectName("originalWidget")
        widgetLayout = QtGui.QVBoxLayout(widget)
        widgetLayout.setSpacing(0)
        widgetLayout.setMargin(0)
        widgetLayout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        frame = QtGui.QFrame()
        frame.setObjectName("originalFrame")
        widgetLayout.addWidget(frame)
        layout = QtGui.QVBoxLayout(frame)
        layout.setObjectName("originalLayout")
        layout.setAlignment(QtCore.Qt.AlignTop)
        textLabel = WTweetLabel(frame)
        textLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        originalItem = self.tweet.original
        try:
            textLabel.setText("@%s: " % originalItem.author.name + self._create_html_url(originalItem.text))
        except:
            #originalItem.text == This tweet deleted by author
            textLabel.setText(self._create_html_url(originalItem.text))
        #textLabel.setWordWrap(True)
        #textLabel.setIndent(0)
        layout.addWidget(textLabel)

        if originalItem.thumbnail_pic:
            layout.addWidget(self._createImageLabel(originalItem.thumbnail_pic))

        counterHorizontalLayout = QtGui.QHBoxLayout()
        counterHorizontalLayout.setObjectName("counterhorizontalLayout")
        horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                                     QtGui.QSizePolicy.Minimum)
        counterHorizontalLayout.addItem(horizontalSpacer)
        retweet = WIconLabel(widget)
        retweet.setObjectName("retweet")
        retweet.setText(str(originalItem.retweets_count))
        retweet.setIcon("./icon/retweets.png")
        retweet.clicked.connect(self._original_retweet)
        counterHorizontalLayout.addWidget(retweet)
        comment = WIconLabel(widget)
        comment.setObjectName("comment")
        comment.setIcon("./icon/comments.png")
        comment.setText(str(originalItem.comments_count))
        comment.clicked.connect(self._original_comment)
        counterHorizontalLayout.addWidget(comment)
        counterHorizontalLayout.setSpacing(6)
        layout.setMargin(8)
        layout.setSpacing(0)
        layout.addLayout(counterHorizontalLayout)
        #layout.setStretch(1, 10)
        #layout.setStretch(2, 100)

        frame.setStyleSheet("""
            QFrame#originalFrame {
                border: 2px solid palette(highlight);
                border-radius: 4px;
                padding: 2px;
            }
        """)

        return widget

    def _createImageLabel(self, thumbnail_pic):
        widget = QtGui.QWidget(self)
        widget.setObjectName("imageLabel")
        widgetLayout = QtGui.QVBoxLayout(widget)
        widgetLayout.setSpacing(0)
        widgetLayout.setMargin(0)
        widgetLayout.setAlignment(QtCore.Qt.AlignCenter)

        frame = QtGui.QFrame()
        frame.setObjectName("imageFrame")
        widgetLayout.addWidget(frame)
        layout = QtGui.QVBoxLayout(frame)
        layout.setObjectName("imageLayout")

        self.imageLabel = WAsyncLabel(widget)
        self.imageLabel.setPixmap(thumbnail_pic)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.clicked.connect(self._showFullImage)

        layout.addWidget(self.imageLabel)
        widgetLayout.addWidget(frame)

        return widget

    @async
    def fetch_open_original_pic(self, thumbnail_pic):
        """Fetch and open original pic from thumbnail pic url.
           Pictures will stored in cache directory. If we already have a same
           name in cache directory, just open it. If we don't, then download it
           first."""

        if self.download_lock:
            return

        self.download_lock = True
        self.commonSignal.emit(lambda: self.imageLabel.setBusy(True))
        original_pic = thumbnail_pic.replace("thumbnail",
                                             "large")  # A simple trick ... ^_^
        localfile = cache_path + original_pic.split("/")[-1]
        if not os.path.exists(localfile):
            urllib.request.urlretrieve(original_pic, localfile)

        self.download_lock = False
        self.commonSignal.emit(lambda: self.imageLabel.setBusy(False))
        os.system("xdg-open %s > /dev/null" % localfile)
        self.imageLoaded.emit()

    def _showFullImage(self):
        self.fetch_open_original_pic(self.imageLabel.url)

    def commonProcessor(self, object):
        object()

    @async
    def _favorite(self):
        try:
            self.client.favorites.create.post(id=self.tweet.id)
            self.commonSignal.emit(lambda: self.favorite.setIcon("./icon/favorites.png"))
        except:
            pass

    def _retweet(self, tweet=None):
        from NewpostWindow import NewpostWindow
        if not tweet:
            tweet = self.tweet
        if tweet.type == TweetItem.RETWEET:
            text = "//@" + tweet.author.name + ":" + tweet.text
        else:
            text = ""
        wecase_new = NewpostWindow("retweet", tweet)
        wecase_new.exec_()

    def _comment(self, tweet=None):
        from NewpostWindow import NewpostWindow
        if not tweet:
            tweet = self.tweet
        if tweet.type == TweetItem.COMMENT:
            self._reply(tweet)
            return

        wecase_new = NewpostWindow("comment", tweet)
        wecase_new.exec_()

    def _reply(self, tweet=None):
        from NewpostWindow import NewpostWindow
        if not tweet:
            tweet = self.tweet
        wecase_new = NewpostWindow("reply", tweet)
        wecase_new.exec_()

    def _original_retweet(self):
        self._retweet(self.tweet.original)

    def _original_comment(self):
        self._comment(self.tweet.original)

    def _create_html_url(self, text):
        url = re.compile(r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""")
        new_text = url.sub( r"""<a href='\1'>\1</a>""", text)
        return new_text
