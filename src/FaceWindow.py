# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented SmileyWindow.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtGui
from Face import FaceModel
from FaceWidget import WFaceListWidget


class FaceWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(FaceWindow, self).__init__(parent)
        self.setupUi(self)
        self.setupModels()
        self.faceName = ""

    def setupUi(self, widget):
        self.resize(533, 288)
        self.gridLayout = QtGui.QGridLayout(self)
        self.faceView = WFaceListWidget(self)
        self.gridLayout.addWidget(self.faceView, 0, 0, 1, 1)
        self.setWindowTitle(self.tr("Choose a smiley"))

    def setupModels(self):
        self.faceModel = FaceModel(self)
        self.faceView.setModel(self.faceModel)
        self.faceView.smileyClicked.connect(self.returnSmileyName)

    def returnSmileyName(self, faceName):
        self.faceName = "[%s]" % faceName
        self.done(True)
