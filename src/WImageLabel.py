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

    def setImageFile(self, path, start=True, width=-1, height=-1):
        self.setMovie(QtGui.QMovie(path), start)

        size = QtCore.QSize(width, height)
        if size.isValid():
            self.sizeHint = lambda: size

    def setMovie(self, movie, start=True):
        super(WImageLabel, self).setMovie(movie)
        start and movie.start()

    def start(self):
        self.movie().start()

    def stop(self):
        self.movie().stop()

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
