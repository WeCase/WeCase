#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented WMovie, a memory-store based QMovie.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui


class WMovie(QtGui.QMovie):

    def __init__(self, filepath, parent=None):
        super().__init__(parent)
        self._fileName = ""

        data = b""
        with open(filepath, "rb") as file:
            self._fileName = file.name
            data = file.read()
        self._imageData = QtCore.QBuffer()
        self._imageData.setData(data)
        self.setDevice(self._imageData)

    def fileName(self):
        return self._fileName
