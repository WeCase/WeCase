#!/usr/bin/env python3


from math import ceil
from PyQt4 import QtCore, QtGui
from WImageLabel import WImageLabel


class WFaceListWidget(QtGui.QWidget):

    smileyClicked = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(WFaceListWidget, self).__init__(parent)

    def setModel(self, model):
        self._model = model
        self._setupUi()

    def _setupTabWidget(self, faces):
        layout = QtGui.QGridLayout()
        tab = QtGui.QWidget()
        tab.setLayout(layout)

        col = self._model.gridSize().width()
        row = self._model.gridSize().height()
        index = 0

        for i in range(row):
            for j in range(col):
                try:
                    face = faces[index]
                    widget = WSmileyWidget(face)
                    widget.smileyClicked.connect(self.smileyClicked)
                except IndexError:
                    widget = QtGui.QWidget()
                layout.addWidget(widget, i, j)
                index += 1
        return tab

    def _setupUi(self):
        self.layout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        self.layout.addWidget(self.tabWidget)

        faces = self._model.items()
        for category, faces in faces.items():
            tab = self._setupTabWidget(faces)
            self.tabWidget.addTab(tab, category)
        self.setLayout(self.layout)


class WSmileyWidget(QtGui.QWidget):

    smileyClicked = QtCore.pyqtSignal(str)

    def __init__(self, smiley, parent=None):
        super(WSmileyWidget, self).__init__(parent)
        self._smiley = smiley
        self.smileyLabel = WImageLabel(self)
        self.smileyLabel.setToolTip(smiley.name)
        self.smileyLabel.setImage(smiley.path)
        self.smileyLabel.clicked.connect(self._smileyClicked)

    def _smileyClicked(self):
        self.smileyClicked.emit(self._smiley.name)
