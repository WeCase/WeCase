#!/usr/bin/env python3


import sys
from PyQt4 import QtCore, QtGui
from WImageLabel import WImageLabel
from WAsyncLabel import WAsyncLabel


class WSwitchLabel(QtGui.QWidget):

    def __init__(self, parent=None):
        super(WSwitchLabel, self).__init__(parent)
        self._imagesList = []
        self._currentImage = None

        self._layout = QtGui.QHBoxLayout(self)

        leftLabel = WImageLabel(self)
        leftLabel.setText("<-")
        leftLabel.clicked.connect(self._last)
        self._layout.addWidget(leftLabel)

        self._imageLabel = WAsyncLabel(self)
        self._layout.addWidget(self._imageLabel)

        rightLabel = WImageLabel(self)
        rightLabel.setText("->")
        rightLabel.clicked.connect(self._next)
        self._layout.addWidget(rightLabel)

        self.setLayout(self._layout)

        self.setImagesUrls(["http://ww3.sinaimg.cn/thumbnail/53761c09jw1e8gjf3u09mj20xc0akt9d.jpg", "http://ww1.sinaimg.cn/thumbnail/61add7e3jw1e8h7wxi1qvj20ad0gogmz.jpg"])

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

    def setPixmap(self, pixmap):
        self._currentImage = pixmap
        self._imageLabel.setPixmap(pixmap)


if __name__ == "__main__":

   App = QtGui.QApplication(sys.argv)
   main = WSwitchLabel()
   main.show()
   App.exec()
