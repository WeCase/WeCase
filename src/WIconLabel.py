#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client, Since 4th, Feb, 2013.
#           This file implemented a label with a icon.
# Copyright: GPL v3 or later.


from PyQt4 import QtCore, QtGui


class WIconLabel(QtGui.QLabel):

    clicked = QtCore.pyqtSignal()
    imageAtLeft = 1
    imageAtRight = 2
    imageAtTop = 3
    imageAtBottom = 4

    def __init__(self, parent=None):
        super(WIconLabel, self).__init__(parent)
        self._icon = ""
        self._icon_code = ""
        self._text = ""
        self._position = self.imageAtLeft

    def text(self):
        return self._text

    def setText(self, text):
        self._text = text
        if self._position != self.imageAtBottom:
            text = "<center>" + self._icon_code + text + "</center>"
        else:
            text = "<center>" + text + self._icon_code + "</center>"
        super(WIconLabel, self).setText(text)

    def icon(self):
        return self._icon

    def setIcon(self, icon):
        self._icon = icon
        if self._position == self.imageAtLeft:
            self._icon_code = "<img src=\"%s\" />" % (icon)
        elif self._position == self.imageAtRight:
            self._icon_code = "<img src=\"%s\" />" % (icon)
        elif self._position == self.imageAtTop:
            self._icon_code = "<img src=\"%s\" />" % (icon) + "<br />"
        elif self._position == self.imageAtBottom:
            self._icon_code = "<br />" + "<img src=\"%s\" />" % (icon)
        self.setText(self._text)

    def position(self):
        return self._position

    def setPosition(self, pos):
        self._position = pos
        self.setIcon(self._icon)

    def mouseReleaseEvent(self, e):
        self.clicked.emit()
