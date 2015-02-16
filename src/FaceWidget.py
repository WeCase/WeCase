# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented a widget for smileies.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


import tarfile
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

        col, row = self._model.grid_size()

        for i in range(row):
            for j in range(col):
                try:
                    face = next(faces)
                    widget = WSmileyWidget(face)
                    widget.smileyClicked.connect(self.smileyClicked)
                except StopIteration:
                    widget = QtGui.QWidget()
                layout.addWidget(widget, i, j)
        return tab

    def _setupUi(self):
        self.layout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        self.layout.addWidget(self.tabWidget)

        for category in self._model.categories():
            faces = self._model.faces_by_category(category)
            tab = self._setupTabWidget(faces)
            self.tabWidget.addTab(tab, category)
        self.setLayout(self.layout)

        self.tabWidget.tabBar().currentChanged.connect(self.turnAnimation)

        self._lastTab = 0
        self.tabWidget.tabBar().setCurrentIndex(0)
        self.turnAnimation(0)

    def turnAnimation(self, index):
        self._turnAnimation(self._lastTab, start=False)
        self._turnAnimation(index)
        self._lastTab = index

    def _turnAnimation(self, index, start=True):
        tab = self.tabWidget.widget(index)
        for index in range(tab.layout().count()):
            widget = tab.layout().itemAt(index).widget()
            try:
                if start:
                    widget.smileyLabel.start()
                else:
                    widget.smileyLabel.stop()
            except AttributeError:
                # a spacer
                pass


class WSmileyWidget(QtGui.QWidget):

    smileyClicked = QtCore.pyqtSignal(str)

    def __init__(self, smiley, parent=None):
        super(WSmileyWidget, self).__init__(parent)
        self._smiley = smiley
        self.smileyLabel = WImageLabel(self)
        self.smileyLabel.setToolTip(smiley.name)
        self.smileyLabel.clicked.connect(self._smileyClicked)

        # Before the animation starts, WImageLabel knows nothing
        # about the size of the image. And we don't want to start
        # it now (for CPU and memory usage).
        # So, we must specific the width and height here.
        faces_tar = tarfile.open(path.myself_path + "faces.tar.gz", "r")
        smiley_file = faces_tar.extractfile(smiley.path)
        faces_tar.close()
        self.smileyLabel.setImageFile(smiley_file, smiley.width, smiley.height)

    def _smileyClicked(self):
        self.smileyClicked.emit(self._smiley.name)
