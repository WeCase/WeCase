#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented WImageLabel.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui


class WImageLabel(QtGui.QLabel):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WImageLabel, self).__init__(parent)
        self._imagePath = None
        self._imageData = None

    def setImageFile(self, path, width=-1, height=-1):
        self._imagePath = path

        size = QtCore.QSize(width, height)
        if size.isValid():
            self.sizeHint = lambda: size

    def start(self):
        if self.movie():
            self._imagePath = self.movie().fileName()
        else:
            image = b""
            with open(self._imagePath, "rb") as file:
                image = file.read()
            self._imageData = QtCore.QBuffer()
            self._imageData.setData(image)
            movie = QtGui.QMovie(parent=self._imageData)
            movie.setDevice(self._imageData)
            self.setMovie(movie)
        self.movie().start()

    def stop(self):
        self.movie().stop()

        # free memory
        self._imageData = None
        self.setMovie(None)

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
