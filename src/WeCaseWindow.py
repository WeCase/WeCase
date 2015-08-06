# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented WeCaseWindow, the mainWindow of WeCase.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


import os
import platform
from WTimer import WTimer
from PyQt4 import QtCore, QtGui
from Tweet import TweetCommonModel, TweetCommentModel, TweetUserModel, TweetTopicModel, TweetFilterModel
from Notify import Notify
from NewpostWindow import NewpostWindow
from SettingWindow import WeSettingsWindow
from AboutWindow import AboutWindow
import const
import path
from WConfigParser import WConfigParser
from WeHack import async, setGeometry, getGeometry, UNUSED
from WObjectCache import WObjectCache
from WeRuntimeInfo import WeRuntimeInfo
from TweetListWidget import TweetListWidget
from AsyncFetcher import AsyncFetcher
from rpweibo import APIError
from WeiboErrorHandler import APIErrorWindow
from LoginInfo import LoginInfo
import logging
import wecase_rc


UNUSED(wecase_rc)


class WeCaseWindow(QtGui.QMainWindow):

    client = None
    uid = None
    timelineLoaded = QtCore.pyqtSignal(int)
    imageLoaded = QtCore.pyqtSignal(str)
    tabBadgeChanged = QtCore.pyqtSignal(int, int)
    tabAvatarFetched = QtCore.pyqtSignal(str)

    def __init__(self, username, parent=None):
        super(WeCaseWindow, self).__init__(parent)

        self.username = username
        LoginInfo().add_account(self.username)

        self.errorWindow = APIErrorWindow(self)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, True)
        self._iconPixmap = {}
        self.setupUi(self)
        self._setupSysTray()
        self.tweetViews = [self.homeView, self.mentionsView, self.commentsView, self.commentsMentionsTab]
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
        self._setupUserTab(self.uid(), False, True)

    def _setupTab(self, view):
        tab = QtGui.QWidget()
        layout = QtGui.QGridLayout(tab)
        layout.addWidget(view)
        view.setParent(tab)
        return tab

    def _setupCommonTab(self, timeline, view, switch=True, protect=False):
        self._prepareTimeline(timeline)
        view.setModel(timeline)
        view.userClicked.connect(self.userClicked)
        view.tagClicked.connect(self.tagClicked)
        tab = self._setupTab(view)
        self.tabWidget.addTab(tab, "")
        if switch:
            self.tabWidget.setCurrentWidget(tab)
        if protect:
            self.tabWidget.tabBar().setProtectTab(tab, True)
        return tab

    def _getSameTab(self, attr, value):
        for i in range(self.tabWidget.count()):
            try:
                tab = self.tabWidget.widget(i).layout().itemAt(0).widget()
                _value = getattr(tab.model(), attr)()
                if _value == value:
                    return i
            except AttributeError:
                pass
        return False

    def _setupUserTab(self, uid, switch=True, myself=False):
        index = self._getSameTab("uid", uid)
        if index:
            if switch:
                self.tabWidget.setCurrentIndex(index)
            return

        view = TweetListWidget()
        _timeline = TweetUserModel(self.client.api("statuses/user_timeline"), uid,
                                   view)
        timeline = TweetFilterModel(_timeline)
        timeline.setModel(_timeline)
        tab = self._setupCommonTab(timeline, view, switch, myself)
        fetcher = AsyncFetcher("".join((path.cache_path, str(self.info["uid"]))))

        def setAvatar(f):
            self._setTabIcon(tab, WObjectCache().open(QtGui.QPixmap, f))

        def fetchAvatar():
            url = self.client.api("users/show").get(uid=uid)["profile_image_url"]
            fetcher.addTask(url, setAvatar)

        fetchAvatar()

    def _setupTopicTab(self, topic, switch=True):
        index = self._getSameTab("topic", topic)
        if index:
            if switch:
                self.tabWidget.setCurrentIndex(index)
            return

        view = TweetListWidget()
        timeline = TweetTopicModel(self.client.api("search/topics"), topic, view)
        tab = self._setupCommonTab(timeline, view, switch, protect=False)
        self._setTabIcon(tab, WObjectCache().open(
            QtGui.QPixmap, ":/IMG/img/topic.jpg"
        ))

    @QtCore.pyqtSlot(object, bool)
    def userClicked(self, userItem, openAtBackend):
        try:
            self._setupUserTab(userItem.id, switch=(not openAtBackend))
        except APIError as e:
            self.errorWindow.raiseException.emit(e)

    @QtCore.pyqtSlot(str, bool)
    def tagClicked(self, str, openAtBackend):
        try:
            self._setupTopicTab(str, switch=(not openAtBackend))
        except APIError as e:
            self.errorWindow.raiseException.emit(e)

    def setupUi(self, mainWindow):
        mainWindow.setWindowIcon(QtGui.QIcon(":/IMG/img/WeCase.svg"))
        mainWindow.setDocumentMode(False)
        mainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks |
                                  QtGui.QMainWindow.AnimatedDocks)

        self.centralwidget = QtGui.QWidget(mainWindow)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabBar(WTabBar(self.tabWidget))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

        self.homeView = TweetListWidget()
        self.homeView.userClicked.connect(self.userClicked)
        self.homeView.tagClicked.connect(self.tagClicked)
        self.homeTab = self._setupTab(self.homeView)
        self.tabWidget.addTab(self.homeTab, "")
        self.tabWidget.tabBar().setProtectTab(self.homeTab, True)

        self.mentionsView = TweetListWidget()
        self.mentionsView.userClicked.connect(self.userClicked)
        self.mentionsView.tagClicked.connect(self.tagClicked)
        self.mentionsTab = self._setupTab(self.mentionsView)
        self.tabWidget.addTab(self.mentionsTab, "")
        self.tabWidget.tabBar().setProtectTab(self.mentionsTab, True)

        self.commentsView = TweetListWidget()
        self.commentsView.userClicked.connect(self.userClicked)
        self.commentsView.tagClicked.connect(self.tagClicked)
        self.commentsTab = self._setupTab(self.commentsView)
        self.tabWidget.addTab(self.commentsTab, "")
        self.tabWidget.tabBar().setProtectTab(self.commentsTab, True)

        self.commentsMentionsView = TweetListWidget()
        self.commentsMentionsView.userClicked.connect(self.userClicked)
        self.commentsMentionsView.tagClicked.connect(self.tagClicked)
        self.commentsMentionsTab = self._setupTab(self.commentsMentionsView)
        self.tabWidget.addTab(self.commentsMentionsTab, "")
        self.tabWidget.tabBar().setProtectTab(self.commentsMentionsTab, True)

        self.verticalLayout.addWidget(self.tabWidget)

        self.widget = QtGui.QWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.widget)

        mainWindow.setCentralWidget(self.centralwidget)

        self.aboutAction = QtGui.QAction(mainWindow)
        self.refreshAction = QtGui.QAction(mainWindow)
        self.logoutAction = QtGui.QAction(mainWindow)
        self.exitAction = QtGui.QAction(mainWindow)
        self.settingsAction = QtGui.QAction(mainWindow)
        self.crashAction = QtGui.QAction(mainWindow)

        self.aboutAction.setIcon(QtGui.QIcon(QtGui.QPixmap("./IMG/img/where_s_my_weibo.svg")))
        self.exitAction.setIcon(QtGui.QIcon(QtGui.QPixmap(":/IMG/img/application-exit.svg")))
        self.settingsAction.setIcon(QtGui.QIcon(QtGui.QPixmap(":/IMG/img/preferences-other.png")))
        self.refreshAction.setIcon(QtGui.QIcon(QtGui.QPixmap(":/IMG/img/refresh.png")))

        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setDefaultUp(False)
        mainWindow.setMenuBar(self.menubar)

        self.mainMenu = QtGui.QMenu(self.menubar)
        self.helpMenu = QtGui.QMenu(self.menubar)
        self.optionsMenu = QtGui.QMenu(self.menubar)

        self.mainMenu.addAction(self.refreshAction)
        self.mainMenu.addSeparator()
        self.mainMenu.addAction(self.logoutAction)
        self.mainMenu.addAction(self.exitAction)
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.crashAction)
        self.optionsMenu.addAction(self.settingsAction)
        self.menubar.addAction(self.mainMenu.menuAction())
        self.menubar.addAction(self.optionsMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())

        self.exitAction.triggered.connect(mainWindow.close)
        self.aboutAction.triggered.connect(mainWindow.showAbout)
        self.settingsAction.triggered.connect(mainWindow.showSettings)
        self.logoutAction.triggered.connect(mainWindow.logout)
        self.refreshAction.triggered.connect(mainWindow.refresh)
        self.crashAction.triggered.connect(mainWindow.crash)

        self.pushButton_refresh = QtGui.QPushButton(self.widget)
        self.pushButton_new = QtGui.QPushButton(self.widget)
        self.pushButton_refresh.clicked.connect(mainWindow.refresh)
        self.pushButton_new.clicked.connect(mainWindow.postTweet)
        self.timelineLoaded.connect(self.moveToTop)
        self.tabBadgeChanged.connect(self.drawNotifyBadge)

        self.refreshAction.setShortcut(QtGui.QKeySequence("F5"))
        self.pushButton_refresh.setIcon(QtGui.QIcon(":/IMG/img/refresh.png"))
        self.pushButton_new.setIcon(QtGui.QIcon(":/IMG/img/new.png"))

        if self.isGlobalMenu():
            self._setupToolBar()
        else:
            self._setupButtonWidget()

        self._setTabIcon(self.homeTab, QtGui.QPixmap(":/IMG/img/sina.png"))
        self._setTabIcon(self.mentionsTab, QtGui.QPixmap(":/IMG/img/mentions.png"))
        self._setTabIcon(self.commentsTab, QtGui.QPixmap(":/IMG/img/comments2.png"))
        self._setTabIcon(self.commentsMentionsTab, QtGui.QPixmap(":/IMG/img/mentions_comments.svg"))

        self.retranslateUi(mainWindow)

    def isGlobalMenu(self):
        if os.environ.get("TOOLBAR") == "1":
            return True
        elif os.environ.get("TOOLBAR") == "0":
            return False
        elif os.environ.get('DESKTOP_SESSION') in ["ubuntu", "ubuntu-2d"]:
            if not os.environ.get("UBUNTU_MENUPROXY"):
                return False
            elif os.environ.get("APPMENU_DISPLAY_BOTH"):
                return False
            else:
                return True
        elif os.environ.get("DESKTOP_SESSION") == "kde-plasma" and platform.linux_distribution()[0] == "Ubuntu":
            return True
        elif platform.system() == "Darwin":
            return True
        return False

    def _setupToolBar(self):
        self.toolBar = QtGui.QToolBar()
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        empty = QtGui.QWidget()
        empty.setSizePolicy(QtGui.QSizePolicy.Expanding,
                            QtGui.QSizePolicy.Preferred)
        self.toolBar.addWidget(empty)
        self.toolBar.addAction(self.refreshAction)
        newAction = self.toolBar.addAction(QtGui.QIcon(":/IMG/img/new.png"),
                                           "New")
        newAction.triggered.connect(self.pushButton_new.clicked)
        self.addToolBar(self.toolBar)

    def _setupButtonWidget(self):
        self.buttonWidget = QtGui.QWidget(self)
        self.buttonLayout = QtGui.QHBoxLayout(self.buttonWidget)
        self.horizontalSpacer = QtGui.QSpacerItem(40, 20,
                                                  QtGui.QSizePolicy.Expanding,
                                                  QtGui.QSizePolicy.Minimum)
        self.buttonLayout.addSpacerItem(self.horizontalSpacer)
        self.buttonLayout.addWidget(self.pushButton_refresh)
        self.buttonLayout.addWidget(self.pushButton_new)

    def resizeEvent(self, event):
        # This is a hack!!!
        if self.isGlobalMenu():
            return
        self.buttonWidget.resize(self.menubar.sizeHint().width(),
                                 self.menubar.sizeHint().height() + 12)
        self.buttonWidget.move(self.width() - self.buttonWidget.width(),
                               self.menubar.geometry().topRight().y() - 5)

    def retranslateUi(self, frm_MainWindow):
        frm_MainWindow.setWindowTitle(self.tr("WeCase"))
        self.mainMenu.setTitle(self.tr("&WeCase"))
        self.helpMenu.setTitle(self.tr("&Help"))
        self.optionsMenu.setTitle(self.tr("&Options"))
        self.aboutAction.setText(self.tr("&About..."))
        self.refreshAction.setText(self.tr("Refresh"))
        self.logoutAction.setText(self.tr("&Log out"))
        self.exitAction.setText(self.tr("&Exit"))
        self.settingsAction.setText(self.tr("&Settings"))
        self.crashAction.setText(self.tr("&Crash"))

    def _setupSysTray(self):
        self.systray = QtGui.QSystemTrayIcon()
        self.systray.activated.connect(self.clickedSystray)
        self.systray.setToolTip("WeCase")
        self.systray.setIcon(QtGui.QIcon(":/IMG/img/WeCase.svg"))
        self.systray.show()

        self.visibleAction = QtGui.QAction(self)
        self.visibleAction.setText(self.tr("&Hide"))
        self.visibleAction.triggered.connect(self._switchVisibility)

        self.sysMenu = QtGui.QMenu(self)
        self.sysMenu.addAction(self.visibleAction)
        self.sysMenu.addAction(self.logoutAction)
        self.sysMenu.addAction(self.exitAction)

        self.systray.setContextMenu(self.sysMenu)

    @QtCore.pyqtSlot(int)
    def clickedSystray(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self._switchVisibility()
        elif reason == QtGui.QSystemTrayIcon.Context:
            pass

    @QtCore.pyqtSlot()
    def _switchVisibility(self):
        if self.isVisible():
            self.hide()
            self.visibleAction.setText(self.tr("&Show"))
        else:
            self.show()
            self.visibleAction.setText(self.tr("&Hide"))

    def _setTabIcon(self, tab, icon):
        pixmap = icon.transformed(QtGui.QTransform().rotate(90))
        icon = QtGui.QIcon(pixmap)
        self._iconPixmap[icon.cacheKey()] = pixmap
        self.tabWidget.setTabIcon(self.tabWidget.indexOf(tab), icon)
        self.tabWidget.setIconSize(QtCore.QSize(24, 24))

    def _prepareTimeline(self, timeline):
        try:
            timeline.setUsersBlacklist(self.usersBlacklist)
            timeline.setTweetsKeywordsBlacklist(self.tweetKeywordsBlacklist)
            timeline.setWordWarKeywords(self.wordWarKeywords)
            timeline.setBlockWordwars(self.blockWordwars)
            timeline.setKeywordsAsRegexs(self.keywordsAsRegex)
        except AttributeError:
            pass
        timeline.load()

    @QtCore.pyqtSlot(int)
    def closeTab(self, index):
        widget = self.tabWidget.widget(index)
        self.tabWidget.removeTab(index)
        widget.deleteLater()

    def init_account(self):
        self.uid()

    def loadConfig(self):
        self.config = WConfigParser(path.myself_path + "WMetaConfig",
                                    path.config_path, "main")
        self.notify_interval = self.config.notify_interval
        self.notify_timeout = self.config.notify_timeout
        self.usersBlacklist = self.config.usersBlacklist
        self.tweetKeywordsBlacklist = self.config.tweetsKeywordsBlacklist
        self.remindMentions = self.config.remind_mentions
        self.remindComments = self.config.remind_comments
        self.wordWarKeywords = self.config.wordWarKeywords
        self.blockWordwars = self.config.blockWordwars
        self.maxRetweets = self.config.maxRetweets
        self.maxTweetsPerUser = self.config.maxTweetsPerUser
        self.mainWindow_geometry = self.config.mainwindow_geometry
        self.keywordsAsRegex = self.config.keywordsAsRegex

    def applyConfig(self):
        try:
            self.timer.stop()
        except AttributeError:
            pass

        self.timer = WTimer(self.show_notify, self.notify_interval)
        self.timer.start()
        self.notify.timeout = self.notify_timeout
        setGeometry(self, self.mainWindow_geometry)

    def setupModels(self):
        self._all_timeline = TweetCommonModel(self.client.api("statuses/home_timeline"), self)
        self.all_timeline = TweetFilterModel(self._all_timeline)
        self.all_timeline.setModel(self._all_timeline)
        self._prepareTimeline(self.all_timeline)

        # extra rules
        self.all_timeline.setMaxRetweets(self.maxRetweets)
        self.all_timeline.setMaxTweetsPerUser(self.maxTweetsPerUser)

        self.homeView.setModel(self.all_timeline)

        self._mentions = TweetCommonModel(self.client.api("statuses/mentions"), self)
        self.mentions = TweetFilterModel(self._mentions)
        self.mentions.setModel(self._mentions)
        self._prepareTimeline(self.mentions)
        self.mentionsView.setModel(self.mentions)

        self._comment_to_me = TweetCommentModel(self.client.api("comments/to_me"), self)
        self.comment_to_me = TweetFilterModel(self._comment_to_me)
        self.comment_to_me.setModel(self._comment_to_me)
        self._prepareTimeline(self.comment_to_me)
        self.commentsView.setModel(self.comment_to_me)

        self._comment_mentions = TweetCommentModel(self.client.api("comments/mentions"), self)
        self.comment_mentions = TweetFilterModel(self._comment_mentions)
        self.comment_mentions.setModel(self._comment_mentions)
        self._prepareTimeline(self.comment_mentions)
        self.commentsMentionsView.setModel(self.comment_mentions)

    @async
    def reset_remind(self):
        typ = ""
        if self.currentTweetView() == self.homeView:
            self.tabBadgeChanged.emit(self.tabWidget.currentIndex(), 0)
        elif self.currentTweetView() == self.mentionsView:
            typ = "mention_status"
            self.tabBadgeChanged.emit(self.tabWidget.currentIndex(), 0)
        elif self.currentTweetView() == self.commentsView:
            typ = "cmt"
            self.tabBadgeChanged.emit(self.tabWidget.currentIndex(), 0)
        elif self.currentTweetView() == self.commentsMentionsView:
            typ = "mention_cmt"
            self.tabBadgeChanged.emit(self.tabWidget.currentIndex(), 0)

        if typ:
            self.client.api("remind/set_count").post(type=typ)

    def get_remind(self, uid):
        """this function is used to get unread_count
        from Weibo API. uid is necessary."""

        reminds = self.client.api("remind/unread_count").get(uid=uid)
        return reminds

    def uid(self):
        """How can I get my uid? here it is"""
        if not self.info.get("uid"):
            self.info["uid"] = self.client.api("account/get_uid").get().uid
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

        if reminds["mention_cmt"] and self.remindMentions:
            msg += self.tr("%d unread @ME comment(s)") % reminds["mention_cmt"] + "\n"
            self.tabBadgeChanged.emit(self.tabWidget.indexOf(self.commentsMentionsTab),
                                      reminds["mention_cmt"])
            reminds_count += 1
        else:
            self.tabBadgeChanged.emit(self.tabWidget.indexOf(self.commentsMentionsTab), 0)

        if reminds_count and reminds_count != self._last_reminds_count:
            self.notify.showMessage(self.tr("WeCase"), msg)
            self._last_reminds_count = reminds_count

    @QtCore.pyqtSlot(int, int)
    def drawNotifyBadge(self, index, count):
        tabIcon = self.tabWidget.tabIcon(index)
        _tabPixmap = self._iconPixmap[tabIcon.cacheKey()]
        tabPixmap = _tabPixmap.transformed(QtGui.QTransform().rotate(-90))
        icon = NotifyBadgeDrawer().draw(tabPixmap, str(count))
        icon = icon.transformed(QtGui.QTransform().rotate(90))
        icon = QtGui.QIcon(icon)
        self._iconPixmap[icon.cacheKey()] = _tabPixmap
        self.tabWidget.setTabIcon(index, icon)

    @QtCore.pyqtSlot()
    def moveToTop(self):
        self.currentTweetView().moveToTop()

    @QtCore.pyqtSlot()
    def showSettings(self):
        wecase_settings = WeSettingsWindow()
        if wecase_settings.exec_():
            self.loadConfig()
            self.applyConfig()

    @QtCore.pyqtSlot()
    def showAbout(self):
        wecase_about = AboutWindow()
        wecase_about.exec_()

    @QtCore.pyqtSlot()
    def logout(self):
        self.close()
        # This is a model dialog, if we exec it before we close MainWindow
        # MainWindow won't close
        from LoginWindow import LoginWindow
        wecase_login = LoginWindow(allow_auto_login=False)
        wecase_login.exec_()

    @QtCore.pyqtSlot()
    def postTweet(self):
        self.wecase_new = NewpostWindow()
        self.wecase_new.userClicked.connect(self.userClicked)
        self.wecase_new.tagClicked.connect(self.tagClicked)
        self.wecase_new.show()

    @QtCore.pyqtSlot()
    def refresh(self):
        tweetView = self.currentTweetView()
        tweetView.model().timelineLoaded.connect(self.moveToTop)
        tweetView.refresh()
        self.reset_remind()

    def currentTweetView(self):
        # The most tricky part of MainWindow.
        return self.tabWidget.currentWidget().layout().itemAt(0).widget()

    def saveConfig(self):
        self.config.mainwindow_geometry = getGeometry(self)
        self.config.save()

    def closeEvent(self, event):
        self.systray.hide()
        self.hide()
        self.saveConfig()
        self.timer.stop(True)
        # Reset uid when the thread exited.
        self.info["uid"] = None
        LoginInfo().remove_account(self.username)
        logging.info("Die")

    @QtCore.pyqtSlot()
    def crash(self):
        raise RuntimeError("User asked to crash")


class NotifyBadgeDrawer():

    def fillEllipse(self, p, x, y, size, extra, brush):
        path = QtGui.QPainterPath()
        path.addEllipse(x, y, size + extra, size)
        p.fillPath(path, brush)

    def drawBadge(self, p, x, y, size, text, brush):
        p.setFont(QtGui.QFont(QtGui.QWidget().font().family(), size * 1 / 2,
                              QtGui.QFont.Bold))

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
            text = "N"

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


class WTabBar(QtGui.QTabBar):

    def __init__(self, parent=None):
        super(WTabBar, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)
        self.__protect = []

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.MiddleButton:
            self.closeTab(e.pos())
        super(WTabBar, self).mouseReleaseEvent(e)

    @QtCore.pyqtSlot(int)
    def contextMenu(self, pos):
        if self.isProtected(pos):
            return

        closeAction = QtGui.QAction(self)
        closeAction.setText(self.tr("&Close"))
        closeAction.triggered.connect(lambda: self.closeTab(pos))

        menu = QtGui.QMenu()
        menu.addAction(closeAction)
        menu.exec(self.mapToGlobal(pos))

    def isProtected(self, pos):
        if self.parent().widget(self.tabAt(pos)) in self.__protect:
            return True
        return False

    def closeTab(self, pos):
        if self.isProtected(pos):
            return False
        self.parent().tabCloseRequested.emit(self.tabAt(pos))
        return True

    def setProtectTab(self, tabWidget, state):
        if state and tabWidget not in self.__protect:
            self.__protect.append(tabWidget)
        elif not state:
            self.__protect.remove(tabWidget)

    def protectTab(self, tabWidget):
        return (tabWidget in self.__protect)
