# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented a Label for fetching the images async.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui
from WImageLabel import WImageLabel
from path import cache_path as down_path
from WObjectCache import WObjectCache
from AsyncFetcher import AsyncFetcher
from WeRuntimeInfo import WeRuntimeInfo


class WAsyncLabel(WImageLabel):

    clicked = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(WAsyncLabel, self).__init__(parent)
        self._url = ""
        self._image = None

        self.fetcher = AsyncFetcher("".join((down_path, str(WeRuntimeInfo()["uid"]))))

        busyIconPixmap = WObjectCache().open(QtGui.QPixmap, ":/IMG/img/busy.gif")
        self.minimumImageHeight = busyIconPixmap.height()
        self.minimumImageWidth = busyIconPixmap.width()

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

    def url(self):
        return self._url

    def setBusy(self, busy):
        if busy:
            # Hack: #74.
            # What's wrong with the busyMovie()? To save the memory,
            # We use a single busyMovie() in the whole program.
            # If the image downloaded here, we'll stop the movie and the
            # busyIcon will disappear. But it may start from somewhere else.
            # The the busyIcon appear again unexpectedly.
            # The quick fix is disconnecting the signal/slot connection
            # when we stop the movie.
            self.animation = WObjectCache().open(QtGui.QMovie, ":/IMG/img/busy.gif")
            self.animation.start()
            self.animation.frameChanged.connect(self.drawBusyIcon)
        else:
            self.clearBusyIcon()

    @QtCore.pyqtSlot()
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
        self.animation.frameChanged.disconnect(self.drawBusyIcon)
        super(WAsyncLabel, self).setPixmap(self._image)

    def _setPixmap(self, path):
        _image = QtGui.QPixmap(path)
        minimalHeight = self.minimumImageHeight
        minimalWidth = self.minimumImageWidth

        if _image.height() < minimalHeight or _image.width() < minimalWidth:
            if _image.height() > minimalHeight:
                height = _image.height()
            else:
                height = minimalHeight

            if _image.width() > minimalWidth:
                width = _image.width()
            else:
                width = minimalWidth

            image = QtGui.QPixmap(width, height)
            painter = QtGui.QPainter(image)
            path = QtGui.QPainterPath()
            path.addRect(0, 0, width, height)
            painter.fillPath(path, QtGui.QBrush(QtCore.Qt.gray))
            painter.drawPixmap((width - _image.width()) / 2,
                               (height - _image.height()) / 2,
                               _image)
            painter.end()
        else:
            image = _image

        self._image = image
        super(WAsyncLabel, self).setPixmap(image)

    def setPixmap(self, url):
        super(WAsyncLabel, self).setMovie(
            WObjectCache().open(QtGui.QMovie, ":/IMG/img/busy.gif")
        )
        self.start()
        if not ("http" in url):
            self._setPixmap(url)
            return
        self._url = url
        self._fetch()

    def _fetch(self):
        self.fetcher.addTask(self._url, self.setPixmap)

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton and self._image:
            self.clicked.emit(QtCore.Qt.LeftButton)
        elif e.button() == QtCore.Qt.MiddleButton and self._image:
            self.clicked.emit(QtCore.Qt.MiddleButton)

    @QtCore.pyqtSlot(int)
    def contextMenu(self, pos):
        if not self._image:
            return
        saveAction = QtGui.QAction(self)
        saveAction.setText(self.tr("&Save"))
        saveAction.triggered.connect(self.save)
        menu = QtGui.QMenu()
        menu.addAction(saveAction)
        menu.exec(self.mapToGlobal(pos))

    @QtCore.pyqtSlot()
    def save(self):
        file = QtGui.QFileDialog.getOpenFileName(self,
                                                 self.tr("Choose a path"))
        self._image.save(file)
