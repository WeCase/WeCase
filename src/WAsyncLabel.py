import os
from time import sleep
from threading import Thread
import urllib.request
import http.client
from PyQt4 import QtCore, QtGui
from const import cache_path as down_path


class WAsyncLabel(QtGui.QLabel):

    clicked = QtCore.pyqtSignal()
    downloaded = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(WAsyncLabel, self).__init__(parent)
        self.url = ""

    def url(self):
        return self.url

    def _setPixmap(self, path):
        super(WAsyncLabel, self).setPixmap(QtGui.QPixmap(path))

    def setPixmap(self, url):
        if not ("http" in url):
            self._setPixmap(url)
            return
        self.url = url
        self.downloaded.connect(self._setPixmap)
        self._fetch_meta()

    def _fetch_meta(self):
        filename = "%s_%s" % (self.url.split('/')[-2],
                              self.url.split('/')[-1])
        Thread(group=None, target=self._fetch,
               args=(self.url, filename)).start()

    def _fetch(self, url, filename):
        while os.path.exists(down_path + filename + ".down"):
            sleep(0.5)
            continue

        if os.path.exists(down_path + filename):
            return self.downloaded.emit(down_path + filename)

        while 1:
            try:
                urllib.request.urlretrieve(url, down_path + filename + ".down")
                break
            except http.client.BadStatusLine:
                continue

        try:
            os.rename(down_path + filename + ".down",
                      down_path + filename)
        except FileNotFoundError:
            pass

        return self.downloaded.emit(down_path + filename)

    def mouseReleaseEvent(self, e):
        self.clicked.emit()
