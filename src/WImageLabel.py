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
        self._image = None

    def setImageFile(self, path, width=-1, height=-1):
        self._image = path

        size = QtCore.QSize(width, height)
        if size.isValid():
            self.sizeHint = lambda: size

    def start(self):
        if self.movie():
            self._image = self.movie().fileName()
        else:
            self.setMovie(QtGui.QMovie(self._image))
        self.movie().start()

    def stop(self):
        self.movie().stop()
        self.setMovie(None)  # free memory

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
