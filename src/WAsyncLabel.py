import os
from time import sleep
import urllib.request
from urllib.error import URLError, ContentTooShortError
from http.client import BadStatusLine
from PyQt4 import QtCore, QtGui
from WImageLabel import WImageLabel
from const import cache_path as down_path
from const import icon
from WeHack import async


class WAsyncLabel(WImageLabel):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WAsyncLabel, self).__init__(parent)
        self._url = ""
        self._image = None

        self.fetcher = WAsyncFetcher(self)
        self.fetcher.fetched.connect(self._setPixmap)
        self.busyIcon = icon("busy.gif")
        self.busyIconPixmap = QtGui.QPixmap(self.busyIcon)

    def url(self):
        return self._url

    def setBusy(self, busy):
        if busy:
            self.animation = QtGui.QMovie(self.busyIcon)
            self.animation.start()
            self.animation.frameChanged.connect(self.drawBusyIcon)
        else:
            self.clearBusyIcon()

    def drawBusyIcon(self):
        image = QtGui.QPixmap(self._image)
        icon = self.animation.currentPixmap()

        height = (image.height() - icon.height()) / 2
        width = (image.width() - icon.width()) / 2
        painter = QtGui.QPainter(image)
        painter.drawPixmap(width, height, icon)
        painter.end()
        super(WAsyncLabel, self).setPixmap(image)

    def clearBusyIcon(self):
        self.animation.stop()
        super(WAsyncLabel, self).setPixmap(self._image)

    def _setPixmap(self, path):
        image = QtGui.QPixmap(path)
        if image.width() < self.busyIconPixmap.width():
            image = image.scaledToWidth(self.busyIconPixmap.width())
        self._image = image
        super(WAsyncLabel, self).setPixmap(image)

    def setPixmap(self, url):
        super(WAsyncLabel, self).setImage(self.busyIcon)
        self.start()
        if not ("http" in url):
            self._setPixmap(url)
            return
        self._url = url
        self._fetch()

    def _formattedFilename(self):
        return "%s_%s" % (self._url.split('/')[-2],
                          self._url.split('/')[-1])

    def _fetch(self):
        self.fetcher.fetch(self._url, self._formattedFilename())

    def mouseReleaseEvent(self, e):
        if self._image:
            self.clicked.emit()


class WAsyncFetcher(QtCore.QObject):

    fetched = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(WAsyncFetcher, self).__init__(parent)

    @async
    def fetch(self, url, filename):
        def delete_tmp():
            try:
                os.remove(down_path + filename + ".down")
                return True
            except OSError:
                return False

        def download():
            while 1:
                try:
                    urllib.request.urlretrieve(url, down_path + filename + ".down")
                    os.rename(down_path + filename + ".down",
                              down_path + filename)
                    return
                except (BadStatusLine, URLError):
                    continue
                except OSError:
                    return

        while 1:
            if os.path.exists(down_path + filename):
                delete_tmp()
                return self.fetched.emit(down_path + filename)
            elif os.path.exists(down_path + filename + ".down"):
                sleep(0.5)
                continue
            else:
                download()
