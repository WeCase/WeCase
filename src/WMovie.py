# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented WMovie, a memory-store based QMovie.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui


class WMovie(QtGui.QMovie):

    def __init__(self, file, parent=None):
        super().__init__(parent)
        # HACK: allow to use a path
        if isinstance(file, str):
            file = open(file, "r")

        data = b""
        data = file.read()
        file.close()
        self._imageData = QtCore.QBuffer()
        self._imageData.setData(data)
        self.setDevice(self._imageData)

    def fileName(self):
        return self._fileName
