import os
import re
import urllib.request
from urllib.error import URLError, ContentTooShortError
from http.client import BadStatusLine
from WeHack import async, start, UNUSED
from weibo import APIError
from PyQt4 import QtCore, QtGui
from Tweet import TweetItem, UserItem
from WIconLabel import WIconLabel
from WTweetLabel import WTweetLabel
from WAsyncLabel import WAsyncLabel
from WImageLabel import WImageLabel
import const
from const import cache_path
from WeRuntimeInfo import WeRuntimeInfo
from Face import FaceModel


class TweetListWidget(QtGui.QWidget):

    userClicked = QtCore.pyqtSignal(UserItem)
    tagClicked = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, without=[]):
        super(TweetListWidget, self).__init__(parent)
        self.tweetListWidget = SimpleTweetListWidget(parent, without)
        self.tweetListWidget.userClicked.connect(self.userClicked)
        self.tweetListWidget.tagClicked.connect(self.tagClicked)
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
            self.setBusy(True, SimpleTweetListWidget.BOTTOM)
            model = self.tweetListWidget.model
            model.next()

    def moveToTop(self):
        self.scrollArea.verticalScrollBar().setSliderPosition(0)

    def setBusy(self, busy, pos):
        self.tweetListWidget.setBusy(busy, pos)

    def model(self):
        return self.tweetListWidget.model

    def refresh(self):
        self.setBusy(True, SimpleTweetListWidget.TOP)
        self.tweetListWidget.model.new()


class SimpleTweetListWidget(QtGui.QWidget):

    TOP = 1
    BOTTOM = 2
    userClicked = QtCore.pyqtSignal(UserItem)
    tagClicked = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, without=[]):
        super(SimpleTweetListWidget, self).__init__(parent)
        self.client = const.client
        self.without = without
        self.setupUi()

    def setupUi(self):
        self.layout = QtGui.QVBoxLayout(self)
        self.setLayout(self.layout)
        self.busyMovie = const.busyMovie()

        #self.searchAction = QtGui.QAction(self)
        #self.searchAction.triggered.connect(self.search)
        #self.searchAction.setShortcut(QtGui.QKeySequence("Ctrl+F"))
        #self.addAction(self.searchAction)

    def setModel(self, model):
        self.model = model
        self.model.rowsInserted.connect(self._rowsInserted)
        self.model.nothingLoaded.connect(self._hideBusyIcon)

    #def search(self):
    #    widget = self.layout.itemAt(0).widget()
    #    if (not self.busy()) and widget.objectName() != "searchEdit":
    #        searchEdit = QtGui.QLineEdit(self)
    #        searchEdit.setObjectName("searchEdit")
    #        self.layout.insertWidget(0, searchEdit)
    #    else:
    #        self.layout.takeAt(0)
    #        widget.setParent(None)

    def _hideBusyIcon(self):
        self.setBusy(False, self.BOTTOM)

    def _rowsInserted(self, parent, start, end):
        UNUSED(parent)  # parent is useless

        self.setBusy(False, self.TOP)
        self.setBusy(False, self.BOTTOM)
        for index in range(start, end + 1):
            item = self.model.get_item(index)
            widget = SingleTweetWidget(item, self.without, self)
            widget.userClicked.connect(self.userClicked)
            widget.tagClicked.connect(self.tagClicked)
            self.layout.insertWidget(index, widget)

    def setupBusyIcon(self):
        busyWidget = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(busyWidget)
        busy = WImageLabel()
        busy.setMovie(self.busyMovie)
        layout.addWidget(busy)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        busyWidget.setLayout(layout)
        return busyWidget

    def busy(self):
        top_widget = self.layout.itemAt(0)
        if top_widget:
            top_widget = top_widget.widget()

        bottom_widget = self.layout.itemAt(self.layout.count() - 1)
        if bottom_widget:
            bottom_widget = bottom_widget.widget()

        if top_widget and top_widget.objectName() == "busyIcon":
            return self.TOP
        elif bottom_widget and bottom_widget.objectName() == "busyIcon":
            return self.BOTTOM
        else:
            return False

    def setBusy(self, busy, pos):
        if pos == self.TOP:
            self._setTopBusy(busy)
        elif pos == self.BOTTOM:
            self._setBottomBusy(busy)

    def _setTopBusy(self, busy):
        if busy and self.busy() != self.TOP:
            busy_widget = self.setupBusyIcon()
            busy_widget.setObjectName("busyIcon")
            self.layout.insertWidget(0, busy_widget)
        elif not busy and self.busy() == self.TOP:
            top_widget = self.layout.itemAt(0).widget()
            self.layout.removeWidget(top_widget)
            top_widget.setParent(None)

    def _setBottomBusy(self, busy):
        if busy and self.busy() != self.BOTTOM:
            busy_widget = self.setupBusyIcon()
            busy_widget.setObjectName("busyIcon")
            self.layout.addWidget(busy_widget)
        elif not busy and self.busy() == self.BOTTOM:
            bottom_widget = self.layout.itemAt(self.layout.count() - 1).widget()
            self.layout.removeWidget(bottom_widget)
            bottom_widget.setParent(None)


class SingleTweetWidget(QtGui.QFrame):

    imageLoaded = QtCore.pyqtSignal()
    userClicked = QtCore.pyqtSignal(UserItem)
    tagClicked = QtCore.pyqtSignal(str)
    commonSignal = QtCore.pyqtSignal(object)

    def __init__(self, tweet=None, without=[], parent=None):
        super(SingleTweetWidget, self).__init__(parent)
        self.commonSignal.connect(self.commonProcessor)
        self._gif_list = {}
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
        self.avatar.clicked.connect(self._userClicked)
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
        self.username.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.verticalLayout.addWidget(self.username)

        self.tweetText = WTweetLabel(self)
        self.tweetText.setObjectName("tweetText")
        self.tweetText.setAlignment(QtCore.Qt.AlignTop)
        self.tweetText.userClicked.connect(self._userTextClicked)
        self.tweetText.tagClicked.connect(self.tagClicked)
        self.verticalLayout.addWidget(self.tweetText)

        if self.tweet.thumbnail_pic and (not "image" in self.without):
            self.imageWidget = self._createImageLabel(self.tweet.thumbnail_pic)
            self.verticalLayout.addWidget(self.imageWidget)

        if self.tweet.original and (not "original" in self.without):
            self.originalLabel = self._createOriginalLabel()
            self.verticalLayout.addWidget(self.originalLabel)

        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 10)

        self.counterHorizontalLayout = QtGui.QHBoxLayout()
        self.counterHorizontalLayout.setObjectName("counterhorizontalLayout")
        self.horizontalSpacer = QtGui.QSpacerItem(40, 20,
                                                  QtGui.QSizePolicy.Expanding,
                                                  QtGui.QSizePolicy.Minimum)
        self.counterHorizontalLayout.addItem(self.horizontalSpacer)

        if WeRuntimeInfo().get("uid") == self.tweet.author.id:
            self.delete = self._createDeleteLabel()
            self.counterHorizontalLayout.addWidget(self.delete)

        if not (self.tweet.type == TweetItem.COMMENT):
            self.retweet = self._createRetweetLabel()
            self.counterHorizontalLayout.addWidget(self.retweet)

            self.comment = self._createCommentLabel()
            self.counterHorizontalLayout.addWidget(self.comment)

            self.favorite = self._createFavoriteLabel()
            self.counterHorizontalLayout.addWidget(self.favorite)

            self.counterHorizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        elif self.tweet.type == TweetItem.COMMENT:
            self.reply = self._createReplyLabel()
            self.counterHorizontalLayout.addWidget(self.reply)

        self.verticalLayout.addLayout(self.counterHorizontalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.setStyleSheet("""
            QFrame#SingleTweetWidget {
                border-bottom: 2px solid palette(highlight);
                border-radius: 0px;
                padding: 2px;
            }
        """)

        self.username.setText(" " + self.tweet.author.name)
        text = QtCore.Qt.escape(self.tweet.text)
        text = self._create_mentions(text)
        text = self._create_html_url(text)
        text = self._create_hashtag(text)
        text = self._create_smiles(text)
        self.tweetText.setHtml(text)
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
        try:
            if self.tweet.type != TweetItem.COMMENT:
                self.time.setText("<a href='%s'>%s</a>" %
                                  (self.tweet.url, self.tweet.time))
            else:
                self.time.setText("<a href='%s'>%s</a>" %
                                  (self.tweet.original.url, self.tweet.time))
            self._setup_timer()
        except:
            # Sometimes, user closed the window and the window
            # has been garbage collected already, but
            # the timer is still running. It will cause a runtime error
            pass

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
        textLabel = WTweetLabel()
        textLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        textLabel.userClicked.connect(self._userTextClicked)
        textLabel.tagClicked.connect(self.tagClicked)
        self.textLabel = textLabel  # Hack: save a reference
        originalItem = self.tweet.original

        text = QtCore.Qt.escape(originalItem.text)
        text = self._create_mentions(text)
        text = self._create_html_url(text)
        text = self._create_hashtag(text)
        text = self._create_smiles(text)
        try:
            authorName = self._create_mentions("@" + originalItem.author.name)
            textLabel.setHtml("%s: %s" % (authorName, text))
        except:
            # originalItem.text == This tweet deleted by author
            textLabel.setHtml(text)
        layout.addWidget(textLabel)

        if originalItem.thumbnail_pic:
            layout.addWidget(self._createImageLabel(originalItem.thumbnail_pic))

        counterHorizontalLayout = QtGui.QHBoxLayout()
        counterHorizontalLayout.setObjectName("counterhorizontalLayout")
        horizontalSpacer = QtGui.QSpacerItem(40, 20,
                                             QtGui.QSizePolicy.Expanding,
                                             QtGui.QSizePolicy.Minimum)
        counterHorizontalLayout.addItem(horizontalSpacer)
        retweet = WIconLabel(widget)
        retweet.setObjectName("retweet")
        retweet.setText(str(originalItem.retweets_count))
        retweet.setIcon(const.myself_path + "/icon/retweets.png")
        retweet.clicked.connect(self._original_retweet)
        counterHorizontalLayout.addWidget(retweet)
        comment = WIconLabel(widget)
        comment.setObjectName("comment")
        comment.setIcon(const.myself_path + "/icon/comments.png")
        comment.setText(str(originalItem.comments_count))
        comment.clicked.connect(self._original_comment)
        counterHorizontalLayout.addWidget(comment)
        counterHorizontalLayout.setSpacing(6)
        layout.setMargin(8)
        layout.setSpacing(0)
        layout.addLayout(counterHorizontalLayout)

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

    def _createFavoriteLabel(self):
        favorite = WIconLabel(self)
        favorite.setIcon(const.myself_path + "/icon/no_favorites.png")
        favorite.clicked.connect(self._favorite)
        return favorite

    def _createRetweetLabel(self):
        retweet = WIconLabel(self)
        retweet.setObjectName("retweet")
        retweet.setText(str(self.tweet.retweets_count))
        retweet.setIcon(const.myself_path + "/icon/retweets.png")
        retweet.clicked.connect(self._retweet)
        return retweet

    def _createCommentLabel(self):
        comment = WIconLabel(self)
        comment.setObjectName("comment")
        comment.setIcon(const.myself_path + "/icon/comments.png")
        comment.setText(str(self.tweet.comments_count))
        comment.clicked.connect(self._comment)
        return comment

    def _createReplyLabel(self):
        reply = WIconLabel(self)
        reply.setObjectName("reply")
        reply.setIcon(const.myself_path + "/icon/retweets.png")
        reply.clicked.connect(self._reply)
        return reply

    def _createDeleteLabel(self):
        delete = WIconLabel(self)
        delete.setObjectName("delete")
        delete.setIcon(const.myself_path + "/icon/deletes.png")
        delete.clicked.connect(self._delete)
        return delete

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
            while True:
                try:
                    urllib.request.urlretrieve(original_pic, localfile)
                    break
                except (BadStatusLine, URLError, ContentTooShortError):
                    continue

        self.download_lock = False
        self.commonSignal.emit(lambda: self.imageLabel.setBusy(False))
        start(localfile)
        self.imageLoaded.emit()

    def _showFullImage(self):
        self.fetch_open_original_pic(self.imageLabel.url())

    def commonProcessor(self, object):
        object()

    @async
    def _favorite(self):
        try:
            self.tweet.favorite()
            self.commonSignal.emit(lambda:
                                       self.favorite.setIcon(
                                           const.myself_path + \
                                           "/icon/favorites.png"))
        except APIError as e:
            self._e = e
            self.commonSignal.emit(lambda: self._handle_api_error(self._e))

    def _retweet(self, tweet=None):
        if not tweet:
            tweet = self.tweet

        self.exec_newpost_window("retweet", tweet)

    def _comment(self, tweet=None):
        if not tweet:
            tweet = self.tweet
        if tweet.type == TweetItem.COMMENT:
            self._reply(tweet)
            return

        self.exec_newpost_window("comment", tweet)

    def _reply(self, tweet=None):
        if not tweet:
            tweet = self.tweet
        self.exec_newpost_window("reply", tweet)

    def _delete(self):
        choice = QtGui.QMessageBox.question(
                self, self.tr("Delete?"),
                self.tr("You can't undo your deletion."),
                QtGui.QMessageBox.Yes,
                QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.No:
            return

        try:
            self.tweet.delete()
        except APIError as e:
            self._handle_api_error(e)
        self.timer.stop()
        self.hide()

    def _original_retweet(self):
        self._retweet(self.tweet.original)

    def _original_comment(self):
        self._comment(self.tweet.original)

    def _create_html_url(self, text):
        COMMON_URL_RE = (r"(?i)\b((?:https?://|www\d{0,3}[.]"
                         r"|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+"
                         r"|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+"
                         r"(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|"
                         r"[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
        SINA_URL_RE = r"(http://t.cn/\w{6,7})"
        regex = re.compile("((%s)|(%s))" % (SINA_URL_RE, COMMON_URL_RE))
        new_text = regex.sub(r"""<a href='\1'>\1</a>""", text)
        return new_text

    def _create_smiles(self, text):
        faceModel = FaceModel()
        faceModel.init()
        for name, path in faceModel.dic().items():
            new_text = text.replace("[%s]" % name, '<img src="%s" />' % path)
            if new_text != text:
                self._create_animation(path)
                text = new_text
        return text

    def _create_mentions(self, text):
        MENTIONS_RE = re.compile('(@[-a-zA-Z0-9_\u4e00-\u9fa5]+)')
        regex = re.compile(MENTIONS_RE)
        new_text = regex.sub(r"""<a href='mentions:///\1'>\1</a>""", text)
        return new_text

    def _create_hashtag(self, text):
        HASHTAG_RE = re.compile("([#]+[a-zA-Z0-9_\u4e00-\u9fa5]+[#])")
        regex = re.compile(HASHTAG_RE)
        new_text = regex.sub(r"""<a href='hashtag:///\1'>\1</a>""", text)
        return new_text

    def _create_animation(self, path):
        movie = QtGui.QMovie(path, parent=self)
        if path in self._gif_list.values():
            # We added it already.
            return
        self._gif_list[movie] = path
        movie.frameChanged.connect(self.drawAnimate)
        movie.start()

    def drawAnimate(self):
        sender = self.sender()
        if isinstance(sender, QtGui.QMovie):
            movie = sender
        else:
            return

        self._addSingleFrame(movie, self.tweetText)
        if self.tweet.type == TweetItem.RETWEET:
            try:
                self._addSingleFrame(movie, self.textLabel)
            except AttributeError:
                pass

    def _addSingleFrame(self, movie, textBrowser):
        document = textBrowser.document()
        document.addResource(QtGui.QTextDocument.ImageResource,
                             QtCore.QUrl(self._gif_list[movie]),
                             movie.currentPixmap())
        # Cause a force refresh
        textBrowser.setLineWrapColumnOrWidth(textBrowser.lineWrapColumnOrWidth())

    def exec_newpost_window(self, action, tweet):
        from NewpostWindow import NewpostWindow
        try:
            self.wecase_new = NewpostWindow(action, tweet)
            self.wecase_new.show()
        except APIError as e:
            self._handle_api_error(e)

    def _handle_api_error(self, exception):
        if exception.error_code == 20101:
            QtGui.QMessageBox.information(self, self.tr("Error"),
                                          self.tr("This tweet have been deleted."))
        elif exception.error_code == 20704:
            QtGui.QMessageBox.information(self, self.tr("Error"),
                                          self.tr("This tweet have been collected already.."))
        else:
            QtGui.QMessageBox.warning(self, self.tr("Unknown Error"),
                                      str(exception))

    def _userClicked(self):
        self.userClicked.emit(self.tweet.author)

    def _userTextClicked(self, user):
        self.userClicked.emit(UserItem({"name": user}))