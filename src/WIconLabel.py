#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client, Since 4th, Feb, 2013.
#           This file implemented a label with a icon.
# Copyright: GPL v3 or later.


from PyQt4 import QtCore, QtGui


class WIconLabel(QtGui.QLabel):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WIconLabel, self).__init__(parent)
        self._icon = ""
        self._text = ""

    def text(self):
        return self._text

    def setText(self, text):
        self._text = text
        text = self._icon + text
        super(WIconLabel, self).setText(text)

    def setIcon(self, icon):
        self._icon = "<img src=\"%s\" />" % (icon)
        self.setText(self._text)

    def mouseReleaseEvent(self, e):
        self.clicked.emit()
