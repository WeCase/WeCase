#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented a label with a icon.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui
from WObjectCache import WObjectCache


class WIconLabel(QtGui.QWidget):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._icon = None
        self._text = None

    def setIcon(self, icon):
        self._icon = WObjectCache().open(QtGui.QPixmap, icon)
        self.update()

    def setText(self, text):
        if self._text is None:
            self._text = QtGui.QStaticText()
        self._text.setText(text)
        self.update()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        if self._icon:
            painter.drawPixmap(0, 0, self._icon)
        if self._text:
            painter.drawStaticText(self._icon.width(), 0, self._text)

    def sizeHint(self):
        if self._text:
            return QtCore.QSize(self._icon.width() + self._text.size().width(), self._icon.height())
        elif self._icon:
            return self._icon.size()
        else:
            return QtCore.QSize(0, 0)

    def mouseReleaseEvent(self, e):
        self.clicked.emit()
