#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented WeCaseWindow, the mainWindow of WeCase.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import http
from time import sleep
from WTimer import WTimer
from PyQt4 import QtCore, QtGui
from Tweet import TweetCommonModel, TweetCommentModel, TweetUserModel
from Notify import Notify
from NewpostWindow import NewpostWindow
from SettingWindow import WeSettingsWindow
from AboutWindow import AboutWindow
import const
from WeCaseConfig import WeCaseConfig
from WeHack import async
from WeRuntimeInfo import WeRuntimeInfo
from TweetListWidget import TweetListWidget
from WAsyncLabel import WAsyncFetcher
import wecase_rc


class WeCaseWindow(QtGui.QMainWindow):

    client = None
    uid = None
    timelineLoaded = QtCore.pyqtSignal(int)
    imageLoaded = QtCore.pyqtSignal(str)
    tabBadgeChanged = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(WeCaseWindow, self).__init__(parent)
        self._iconPixmap = {}
        self.setupUi(self)
        self._setupSysTray()
        self.tweetViews = [self.homeView, self.mentionsView, self.commentsView]
        self.info = WeRuntimeInfo()
        self.client = const.client
        self.loadConfig()
        self.init_account()
        self.setupModels()
        self.IMG_AVATAR = -2
        self.IMG_THUMB = -1
        self.notify = Notify(timeout=self.notify_timeout)
        self.applyConfig()
        self.download_lock = []
        self._last_reminds_count = 0
        self._setupUserTab(self.uid(), False)

    def _setupTab(self, view):
        tab = QtGui.QWidget()
        layout = QtGui.QGridLayout(tab)
        layout.addWidget(view)
        return tab

    def _setupUserTab(self, uid, switch=True):
        view = TweetListWidget(self)
        timeline = TweetUserModel(self.client.statuses.user_timeline, uid, self)
        timeline.setUsersBlacklist(self.usersBlacklist)
        timeline.setTweetsKeywordsBlacklist(self.tweetKeywordsBlacklist)
        timeline.load()
        view.setModel(timeline)
        tab = self._setupTab(view)
        fetcher = WAsyncFetcher()
        f = fetcher.down(self.client.users.show.get(uid=uid)["profile_image_url"])
        self.tabWidget.addTab(tab, "")
        image = QtGui.QPixmap(f)
        self._setTabIcon(tab, image)
        if switch:
            self.tabWidget.setCurrentWidget(tab)

    def userClicked(self, userItem):
        self._setupUserTab(userItem.id)

    def setupUi(self, mainWindow):
        mainWindow.resize(330, 637)
        mainWindow.setWindowIcon(QtGui.QIcon(":/IMG/img/WeCase.svg"))
        mainWindow.setDocumentMode(False)
        mainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks |
                                  QtGui.QMainWindow.AnimatedDocks)

        self.centralwidget = QtGui.QWidget(mainWindow)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(True)

        self.homeView = TweetListWidget()
        self.homeView.userClicked.connect(self.userClicked)
        self.homeTab = self._setupTab(self.homeView)
        self.tabWidget.addTab(self.homeTab, "")

        self.mentionsView = TweetListWidget()
        self.mentionsView.userClicked.connect(self.userClicked)
        self.mentionsTab = self._setupTab(self.mentionsView)
        self.tabWidget.addTab(self.mentionsTab, "")

        self.commentsView = TweetListWidget()
        self.commentsView.userClicked.connect(self.userClicked)
        self.commentsTab = self._setupTab(self.commentsView)
        self.tabWidget.addTab(self.commentsTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                       QtGui.QSizePolicy.Fixed)
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 30))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        spacerItem = QtGui.QSpacerItem(40, 20,
                                       QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)

        spacerItem1 = QtGui.QSpacerItem(40, 20,
                                        QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)

        self.pushButton_refresh = QtGui.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_refresh, 0, 1, 1, 1)
        self.pushButton_new = QtGui.QPushButton(self.widget)
        self.gridLayout.addWidget(self.pushButton_new, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 315, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Preferred)
        self.menubar.setSizePolicy(sizePolicy)
#        self.menubar.setMinimumSize(QtCore.QSize(0, 0))
        self.menubar.setDefaultUp(False)
        self.menu_WeCase = QtGui.QMenu(self.menubar)
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuO_ptions = QtGui.QMenu(self.menubar)
        mainWindow.setMenuBar(self.menubar)
        self.action_About = QtGui.QAction(mainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/IMG/img/where_s_my_weibo.svg"))
        self.action_About.setIcon(icon1)
        self.action_Refresh = QtGui.QAction(mainWindow)
        self.action_Log_out = QtGui.QAction(mainWindow)
        self.action_Exit = QtGui.QAction(mainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/IMG/img/application-exit.svg"))
        self.action_Exit.setIcon(icon2)
        self.action_Settings = QtGui.QAction(mainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/IMG/img/preferences-other.png"))
        self.action_Settings.setIcon(icon3)
        self.menu_WeCase.addAction(self.action_Refresh)
        self.menu_WeCase.addSeparator()
        self.menu_WeCase.addAction(self.action_Log_out)
        self.menu_WeCase.addAction(self.action_Exit)
        self.menuHelp.addAction(self.action_About)
        self.menuO_ptions.addAction(self.action_Settings)
        self.menubar.addAction(self.menu_WeCase.menuAction())
        self.menubar.addAction(self.menuO_ptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        self.action_Exit.triggered.connect(mainWindow.close)
        self.action_About.triggered.connect(mainWindow.showAbout)
        self.action_Settings.triggered.connect(mainWindow.showSettings)
        self.action_Log_out.triggered.connect(mainWindow.logout)
        self.action_Refresh.triggered.connect(mainWindow.refresh)

        self.pushButton_refresh.clicked.connect(mainWindow.refresh)
        self.pushButton_new.clicked.connect(mainWindow.postTweet)
        self.timelineLoaded.connect(self.moveToTop)
        self.tabBadgeChanged.connect(self.drawNotifyBadge)

        self.action_Refresh.setShortcut(QtGui.QKeySequence("F5"))
        self.pushButton_new.setParent(self)
        self.pushButton_refresh.setParent(self)
        self.pushButton_refresh.setText("")
        self.pushButton_refresh.setIcon(QtGui.QIcon(const.icon("refresh.png")))
        self.pushButton_new.setText("")
        self.pushButton_new.setIcon(QtGui.QIcon(const.icon("new.png")))
        self.buttonWidget = QtGui.QWidget()
        self.buttonLayout = QtGui.QHBoxLayout(self.buttonWidget)
        self.buttonLayout.addWidget(self.pushButton_refresh)
        self.buttonLayout.addWidget(self.pushButton_new)
        self.menubar.setCornerWidget(self.buttonWidget)

        self._setTabIcon(self.homeTab, QtGui.QPixmap(const.icon("sina.png")))
        self._setTabIcon(self.mentionsTab, QtGui.QPixmap(const.icon("mentions.png")))
        self._setTabIcon(self.commentsTab, QtGui.QPixmap(const.icon("comments2.png")))

    def retranslateUi(self, frm_MainWindow):
        frm_MainWindow.setWindowTitle(self.tr("WeCase"))
        self.pushButton_refresh.setText(self.tr("&Refresh"))
        self.pushButton_new.setText(self.tr("&New Weibo"))
        self.menu_WeCase.setTitle(self.tr("&WeCase"))
        self.menuHelp.setTitle(self.tr("&Help"))
        self.menuO_ptions.setTitle(self.tr("&Options"))
        self.action_About.setText(self.tr("&About..."))
        self.action_Refresh.setText(self.tr("&Refresh"))
        self.action_Log_out.setText(self.tr("&Log out"))
        self.action_Exit.setText(self.tr("&Exit"))
        self.action_Settings.setText(self.tr("&Settings"))

    def _setupSysTray(self):
        self.systray = QtGui.QSystemTrayIcon()
        self.systray.activated.connect(self.clickedSystray)
        self.systray.setToolTip("WeCase")
        self.systray.setIcon(QtGui.QIcon(":/IMG/img/WeCase.svg"))
        self.systray.show()

    def clickedSystray(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def _setTabIcon(self, tab, icon):
        pixmap = icon.transformed(QtGui.QTransform().rotate(90))
        icon = QtGui.QIcon(pixmap)
        self._iconPixmap[icon.cacheKey()] = pixmap
        self.tabWidget.setTabIcon(self.tabWidget.indexOf(tab), icon)
        self.tabWidget.setIconSize(QtCore.QSize(24, 24))

    def init_account(self):
        self.uid()

    def loadConfig(self):
        self.config = WeCaseConfig(const.config_path)
        self.notify_interval = self.config.notify_interval
        self.notify_timeout = self.config.notify_timeout
        self.usersBlacklist = self.config.usersBlacklist
        self.tweetKeywordsBlacklist = self.config.tweetsKeywordsBlacklist
        self.remindMentions = self.config.remind_mentions
        self.remindComments = self.config.remind_comments

    def applyConfig(self):
        try:
            self.timer.stop_event.set()
        except AttributeError:
            pass

        self.timer = WTimer(self.notify_interval, self.show_notify)
        self.timer.start()
        self.notify.timeout = self.notify_timeout

    def setupModels(self):
        self.all_timeline = TweetCommonModel(self.client.statuses.home_timeline, self)
        self.all_timeline.setUsersBlacklist(self.usersBlacklist)
        self.all_timeline.setTweetsKeywordsBlacklist(self.tweetKeywordsBlacklist)
        self.all_timeline.load()
        self.homeView.setModel(self.all_timeline)

        self.mentions = TweetCommonModel(self.client.statuses.mentions, self)
        self.mentions.setUsersBlacklist(self.usersBlacklist)
        self.mentions.setTweetsKeywordsBlacklist(self.tweetKeywordsBlacklist)
        self.mentions.load()
        self.mentionsView.setModel(self.mentions)

        self.comment_to_me = TweetCommentModel(self.client.comments.to_me, self)
        self.comment_to_me.setUsersBlacklist(self.usersBlacklist)
        self.comment_to_me.setTweetsKeywordsBlacklist(self.tweetKeywordsBlacklist)
        self.comment_to_me.load()
        self.commentsView.setModel(self.comment_to_me)

    @async
    def reset_remind(self):
        if self.currentTweetView() == self.homeView:
            self.tabBadgeChanged.emit(self.tabWidget.currentIndex(), 0)
        elif self.currentTweetView() == self.mentionsView:
            self.client.remind.set_count.post(type="mention_status")
            self.tabBadgeChanged.emit(self.tabWidget.currentIndex(), 0)
        elif self.currentTweetView() == self.commentsView:
            self.client.remind.set_count.post(type="cmt")
            self.tabBadgeChanged.emit(self.tabWidget.currentIndex(), 0)

    def get_remind(self, uid):
        """this function is used to get unread_count
        from Weibo API. uid is necessary."""

        while 1:
            try:
                reminds = self.client.remind.unread_count.get(uid=uid)
                break
            except http.client.BadStatusLine:
                sleep(0.2)
                continue
        return reminds

    def uid(self):
        """How can I get my uid? here it is"""
        if not self.info.get("uid"):
            self.info["uid"] = self.client.account.get_uid.get().uid
        return self.info["uid"]

    def show_notify(self):
        # This function is run in another thread by WTimer.
        # Do not modify UI directly. Send signal and react it in a slot only.
        # We use SIGNAL self.tabTextChanged and SLOT self.setTabText()
        # to display unread count

        reminds = self.get_remind(self.uid())
        msg = self.tr("You have:") + "\n"
        reminds_count = 0

        if reminds['status'] != 0:
            # Note: do NOT send notify here, or users will crazy.
            self.tabBadgeChanged.emit(self.tabWidget.indexOf(self.homeTab),
                                      reminds['status'])

        if reminds['mention_status'] and self.remindMentions:
            msg += self.tr("%d unread @ME") % reminds['mention_status'] + "\n"
            self.tabBadgeChanged.emit(self.tabWidget.indexOf(self.mentionsTab),
                                      reminds['mention_status'])
            reminds_count += 1
        else:
            self.tabBadgeChanged.emit(self.tabWidget.indexOf(self.mentionsTab), 0)

        if reminds['cmt'] and self.remindComments:
            msg += self.tr("%d unread comment(s)") % reminds['cmt'] + "\n"
            self.tabBadgeChanged.emit(self.tabWidget.indexOf(self.commentsTab),
                                      reminds['cmt'])
            reminds_count += 1
        else:
            self.tabBadgeChanged.emit(self.tabWidget.indexOf(self.commentsTab), 0)

        if reminds_count and reminds_count != self._last_reminds_count:
            self.notify.showMessage(self.tr("WeCase"), msg)
            self._last_reminds_count = reminds_count

    def drawNotifyBadge(self, index, count):
        tabIcon = self.tabWidget.tabIcon(index)
        _tabPixmap = self._iconPixmap[tabIcon.cacheKey()]
        tabPixmap = _tabPixmap.transformed(QtGui.QTransform().rotate(-90))
        icon = NotifyBadgeDrawer().draw(tabPixmap, str(count))
        icon = icon.transformed(QtGui.QTransform().rotate(90))
        icon = QtGui.QIcon(icon)
        self._iconPixmap[icon.cacheKey()] = _tabPixmap
        self.tabWidget.setTabIcon(index, icon)

    def moveToTop(self):
        self.currentTweetView().moveToTop()

    def showSettings(self):
        wecase_settings = WeSettingsWindow()
        if wecase_settings.exec_():
            self.loadConfig()
            self.applyConfig()

    def showAbout(self):
        wecase_about = AboutWindow()
        wecase_about.exec_()

    def logout(self):
        self.info["uid"] = ""
        self.close()
        # This is a model dialog, if we exec it before we close MainWindow
        # MainWindow won't close
        from LoginWindow import LoginWindow
        wecase_login = LoginWindow(allow_auto_login=False)
        wecase_login.exec_()

    def postTweet(self):
        wecase_new = NewpostWindow()
        wecase_new.exec_()

    def refresh(self):
        tweetView = self.currentTweetView()
        tweetView.model().timelineLoaded.connect(self.moveToTop)
        tweetView.refresh()
        self.reset_remind()

    def currentTweetView(self):
        # The most tricky part of MainWindow.
        return self.tabWidget.currentWidget().layout().itemAt(0).widget()

    def closeEvent(self, event):
        self.timer.stop_event.set()


class NotifyBadgeDrawer():

    def fillEllipse(self, p, x, y, size, extra, brush):
        path = QtGui.QPainterPath()
        path.addEllipse(x, y, size + extra, size)
        p.fillPath(path, brush)

    def drawBadge(self, p, x, y, size, text, brush):
        p.setFont(QtGui.QFont(QtGui.QWidget().font().family(), size * 1 / 2,
                              QtGui.QFont.Bold))

        # Method 1:
        #while (size - p.fontMetrics().width(text) < 6):
        #    pointSize = p.font().pointSize() - 1
        #    if pointSize < 6:
        #        weight = QtGui.QFont.Normal
        #    else:
        #        weight = QtGui.QFont.Bold
        #    p.setFont(QtGui.QFont(p.font().family(), p.font().pointSize() - 1, weight))
        # Method 2:
        extra = (len(text) - 1) * 10
        x -= extra

        shadowColor = QtGui.QColor(0, 0, 0, size)
        self.fillEllipse(p, x + 1, y, size, extra, shadowColor)
        self.fillEllipse(p, x - 1, y, size, extra, shadowColor)
        self.fillEllipse(p, x, y + 1, size, extra, shadowColor)
        self.fillEllipse(p, x, y - 1, size, extra, shadowColor)

        p.setPen(QtGui.QPen(QtCore.Qt.white, 2))
        self.fillEllipse(p, x, y, size - 3, extra, brush)
        p.drawEllipse(x, y, size - 3 + extra, size - 3)

        p.setPen(QtGui.QPen(QtCore.Qt.white, 1))
        p.drawText(x, y, size - 3 + extra, size - 3, QtCore.Qt.AlignCenter, text)

    def draw(self, _pixmap, text):
        pixmap = QtGui.QPixmap(_pixmap)
        if text == "0":
            return pixmap
        if len(text) > 2:
            text = ".."

        size = 15
        redGradient = QtGui.QRadialGradient(0.0, 0.0, 17.0, size - 3, size - 3)
        redGradient.setColorAt(0.0, QtGui.QColor(0xe0, 0x84, 0x9b))
        redGradient.setColorAt(0.5, QtGui.QColor(0xe9, 0x34, 0x43))
        redGradient.setColorAt(1.0, QtGui.QColor(0xec, 0x0c, 0x00))

        topRight = pixmap.rect().topRight()
        # magic, don't touch
        offset = topRight.x() - size / 2 - size / 4 - size / 7.5

        p = QtGui.QPainter(pixmap)
        p.setRenderHint(QtGui.QPainter.TextAntialiasing)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        self.drawBadge(p, offset, 0, size, text, QtGui.QBrush(redGradient))
        p.end()

        return pixmap