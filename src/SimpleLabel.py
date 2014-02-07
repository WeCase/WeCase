#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client, Since 4th, Feb, 2013.
#           This file implemented a very simple QLabel-like label.
#
#           The label designed as the time label in SingleTweetWidget,
#           which needs to create many instance and update very often.
#           Therefore, we made it as simple as possible,
#           there were hardcoded values and depends on overmuch assertion
#           condition to work correctly. It can reduce ~5 MB of memory usage
#           when WeCase just started.
#
#           DO NOT FOLLOW THIS PRACTICE in your code or IN THE OTHER PARTS
#           OF WeCase. FOREVER!
# Copyright: GPL v3 or later.


from PyQt4 import QtCore, QtGui
from WeHack import openLink


class SimpleLabel(QtGui.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        self._link = ""

        self._doc = QtGui.QTextDocument()
        self._doc.setIndentWidth(0)
        self._doc.setDocumentMargin(0)

        self._ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()

    def mousePressEvent(self, e):
        openLink(self._link)

    def mouseMoveEvent(self, e):
        if self.rect().contains(e.pos()):
            self.setCursor(QtCore.Qt.PointingHandCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)

    def setText(self, html):
        # Assert:
        # The text is an html tag: <a href='$0'>$1</a>,
        # $0 never changes, because it is the link of a tweet,
        # $1 changes very often, because it is a timer which is counts since
        # the creation time.
        self._doc.setHtml(html)
        self.adjustSize()
        self.repaint()

        if self._link:
            # $0 never changes, don't spend CPU time on re-counting.
            return

        # len("<a href='") == 9
        # 9 + len("http://weibo.com/") == 26
        end = 26
        rest = html[end:]
        for char in rest:
            if char == "'":
                break
            end += 1
        self._link = html[9:end]

    def paintEvent(self, e):
        # parent paintEvent() will hide current tooltip, don't let it happens.
        # super().paintEvent(e)
        painter = QtGui.QPainter(self)
        self._doc.documentLayout().draw(painter, self._ctx)

    def sizeHint(self):
        return QtCore.QSize(self._doc.size().width(), self._doc.size().height())
