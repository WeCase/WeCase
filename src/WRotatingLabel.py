import os
from PyQt4 import QtCore, QtGui
from const import myself_path


class WRotatingLabel(QtGui.QLabel):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WRotatingLabel, self).__init__(parent)
        self._pixmap = None
        self.rotating = QtCore.QTimer(self)
        self.rotating.timeout.connect(self.drawRotatingImage)
        self.degress = 0

    def setRotating(self, state):
        if state:
            self.rotating.start(20)
        else:
            self.rotating.stop()

    def drawRotatingImage(self):
        rotated_pixmap = self._pixmap.transformed(QtGui.QTransform().rotate(self.degress))
        super(WRotatingLabel, self).setPixmap(rotated_pixmap)
        self.degress += 60
        self.degress %= 360

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        super(WRotatingLabel, self).setPixmap(pixmap)

    def mouseReleaseEvent(self, e):
        self.clicked.emit()
