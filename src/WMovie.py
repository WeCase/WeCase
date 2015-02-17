# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented WMovie, a memory-store based QMovie.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui


class WMovie(QtGui.QMovie):

    def __init__(self, file, parent=None):
        super().__init__(parent)

        # HACK: allow to use a path
        need_close = False
        if isinstance(file, str):
            # we only need to close files that were opened by us
            need_close = True
            file = open(file, "r")

        file.seek(0)
        data = file.read()

        if need_close:
            file.close()

        self._fileName = file.name
        self._imageData = QtCore.QBuffer()
        self._imageData.setData(data)
        self.setDevice(self._imageData)

    def fileName(self):
        return self._fileName
