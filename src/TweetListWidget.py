import os
import urllib.request
from threading import Thread
from PyQt4 import QtCore, QtGui
from Tweet import TweetItem
from WIconLabel import WIconLabel
from WTweetLabel import WTweetLabel
from WAsyncLabel import WAsyncLabel
from NewpostWindow import NewpostWindow
from const import cache_path


class TweetListWidget(QtGui.QWidget):

    def __init__(self, client=None, parent=None):
        super(TweetListWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.layout = QtGui.QVBoxLayout(self)
        self.setLayout(self.layout)

    def setModel(self, model):
        self.model = model
        print("Set %s as the model" % (model))
        self.model.rowsInserted.connect(self._rowsInserted)

    def _rowsInserted(self, parent, start, end):
        for index in range(start, end + 1):
            item = self.model.get_item(index)
            self.layout.insertWidget(index, SingleTweetWidget(self.client, item))


class SingleTweetWidget(QtGui.QFrame):

    imageLoaded = QtCore.pyqtSignal()

    def __init__(self, client=None, tweet=None, parent=None):
        super(SingleTweetWidget, self).__init__(parent)
        self.tweet = tweet
        self.client = client
        self.setObjectName("SingleTweetWidget")
        self.setupUi()
        self.download_lock = False

    def setupUi(self):
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
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

        if self.tweet.thumbnail_pic:
            self.imageWidget = self._createImageLabel(self.tweet.thumbnail_pic)
            self.verticalLayout.addWidget(self.imageWidget)

        if self.tweet.original:
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
            self.retweet.setText(self.tweet.retweets_count)
            self.retweet.setIcon("./icon/retweets.png")
            self.retweet.clicked.connect(self._retweet)
            self.counterHorizontalLayout.addWidget(self.retweet)

            self.comment = WIconLabel(self)
            self.comment.setObjectName("comment")
            self.comment.setIcon("./icon/comments.png")
            self.comment.setText(self.tweet.comments_count)
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
        if self.tweet.type != TweetItem.COMMENT:
            self.time.setText("<a href='%s'>%s</a>" % (self.tweet.url, self.tweet.time))
        else:
            self.time.setText(self.tweet.time)
        self.tweetText.setText(self.tweet.text)

    def _createOriginalLabel(self):
        widget = QtGui.QWidget(self)
        widget.setObjectName("originalWidget")
        widgetLayout = QtGui.QVBoxLayout(widget)
        widgetLayout.setSpacing(0)
        widgetLayout.setMargin(0)
        widgetLayout.setAlignment(QtCore.Qt.AlignCenter)

        frame = QtGui.QFrame()
        frame.setObjectName("originalFrame")
        widgetLayout.addWidget(frame)
        layout = QtGui.QVBoxLayout(frame)
        layout.setObjectName("originalLayout")
        textLabel = WTweetLabel(frame)
        textLabel.setAlignment(QtCore.Qt.AlignCenter)
        originalItem = self.tweet.original
        try:
            textLabel.setText("@%s: " % originalItem.author.name + originalItem.text)
        except:
            #originalItem.text == This tweet deleted by author
            textLabel.setText(originalItem.text)
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
        retweet.setText(originalItem.retweets_count)
        retweet.setIcon("./icon/retweets.png")
        retweet.clicked.connect(self._original_retweet)
        counterHorizontalLayout.addWidget(retweet)
        comment = WIconLabel(widget)
        comment.setObjectName("comment")
        comment.setIcon("./icon/comments.png")
        comment.setText(originalItem.comments_count)
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

    def fetch_open_original_pic(self, thumbnail_pic):
        """Fetch and open original pic from thumbnail pic url.
           Pictures will stored in cache directory. If we already have a same
           name in cache directory, just open it. If we don't, then download it
           first."""

        if self.download_lock:
            return

        self.download_lock = True
        original_pic = thumbnail_pic.replace("thumbnail",
                                             "large")  # A simple trick ... ^_^
        localfile = cache_path + original_pic.split("/")[-1]
        if not os.path.exists(localfile):
            urllib.request.urlretrieve(original_pic, localfile)

        self.download_lock = False
        os.popen("xdg-open " + localfile)  # xdg-open is common?
        self.imageLoaded.emit()

    def _showFullImage(self):
        thumbnail_pic = self.imageLabel.url
        Thread(group=None, target=self.fetch_open_original_pic,
                         args=(thumbnail_pic,)).start()

    def _favorite(self):
        try:
            self.client.favorites.create.post(id=int(self.tweet.id))
            self.favorite.setIcon("./icon/favorites.png")
        except:
            pass

    def _retweet(self, tweet=None):
        if not tweet:
            tweet = self.tweet
        if tweet.type == TweetItem.RETWEET:
            text = "//@" + tweet.author.name + ":" + tweet.text
        else:
            text = ""
        wecase_new = NewpostWindow(action="retweet",
                                   id=int(tweet.id),
                                   text=text)
        wecase_new.client = self.client
        wecase_new.exec_()

    def _comment(self, tweet=None):
        if not tweet:
            tweet = self.tweet
        if tweet.type == TweetItem.COMMENT:
            self._reply(tweet)
            return

        wecase_new = NewpostWindow(action="comment",
                                   id=int(tweet.id))
        wecase_new.client = self.client
        wecase_new.exec_()

    def _reply(self, tweet=None):
        if not tweet:
            tweet = self.tweet
        wecase_new = NewpostWindow(action="reply",
                                   id=int(tweet.original.id),
                                   cid=int(tweet.id))
        wecase_new.client = self.client
        wecase_new.exec_()

    def _original_retweet(self):
        self._retweet(self.tweet.original)

    def _original_comment(self):
        self._comment(self.tweet.original)
