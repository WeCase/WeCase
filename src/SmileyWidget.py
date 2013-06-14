#!/usr/bin/env python3


from math import ceil
from PyQt4 import QtCore, QtGui
from WIconLabel import WIconLabel


class WSmileyListWidget(QtGui.QWidget):

    smileyClicked = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(WSmileyListWidget, self).__init__(parent)

    def setModel(self, model):
        self._model = model
        self._setupUi()

    def _setupUi(self):
        # The values are hardcoded, just keep them.
        self.layout = QtGui.QGridLayout()

        items = self._model.items()
        col = 13
        row = ceil(len(items) / 13) - 1

        index = 0
        for i in range(0, row):
            for j in range(0, col):
                item = items[index]
                widget = WSmileyWidget(item)
                widget.smileyClicked.connect(self.smileyClicked)
                self.layout.addWidget(widget, i, j)
                index += 1
        self.setLayout(self.layout)


class WSmileyWidget(QtGui.QWidget):

    smileyClicked = QtCore.pyqtSignal(str)

    def __init__(self, smiley, parent=None):
        super(WSmileyWidget, self).__init__(parent)
        self._smiley = smiley
        self.smileyLabel = WIconLabel(self)
        self.smileyLabel.setToolTip(smiley.name)
        self.smileyLabel.setIcon(smiley.path)
        self.smileyLabel.setPosition(WIconLabel.imageAtTop)
        self.smileyLabel.clicked.connect(self._smileyClicked)

    def _smileyClicked(self):
        self.smileyClicked.emit(self._smiley.name)
