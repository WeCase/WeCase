#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented a label allowing to switch
#           from multiple images.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui
from WImageLabel import WImageLabel
from WAsyncLabel import WAsyncLabel


class WSwitchLabel(QtGui.QWidget):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WSwitchLabel, self).__init__(parent)
        self._imagesList = []
        self._currentImage = None

        self._layout = QtGui.QHBoxLayout(self)

        self._leftLabel = WImageLabel(self)
        self._leftLabel.setText("<-")
        self._leftLabel.clicked.connect(self._last)
        self._layout.addWidget(self._leftLabel)

        self._imageLabel = WAsyncLabel(self)
        self._imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self._imageLabel.clicked.connect(self.clicked)
        self._layout.addWidget(self._imageLabel)

        self._rightLabel = WImageLabel(self)
        self._rightLabel.setText("->")
        self._rightLabel.clicked.connect(self._next)
        self._layout.addWidget(self._rightLabel)

        self.setLayout(self._layout)

    def _last(self):
        currentIndex = self._imagesList.index(self._currentImage)
        if currentIndex >= 1:
            self.setPixmap(self._imagesList[currentIndex - 1])

    def _next(self):
        currentIndex = self._imagesList.index(self._currentImage)
        if currentIndex < len(self._imagesList) - 1:
            self.setPixmap(self._imagesList[currentIndex + 1])

    def setImagesUrls(self, urls):
        self._imagesList = urls
        self.setPixmap(self._imagesList[0])

        if len(urls) == 1:
            self._leftLabel.hide()
            self._rightLabel.hide()
        elif len(urls) >= 1:
            self._leftLabel.show()
            self._rightLabel.show()

    def setPixmap(self, pixmap):
        self._currentImage = pixmap
        self._imageLabel.setPixmap(pixmap)

    def __getattr__(self, attr):
        return eval("self._imageLabel." + attr)
