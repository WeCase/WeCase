#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented SmileyWindow.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


from PyQt4 import QtGui
from Face import FaceModel, FaceItem
from FaceWindow_ui import Ui_FaceWindow
import const


class FaceWindow(QtGui.QDialog, Ui_FaceWindow):
    def __init__(self, parent=None):
        super(FaceWindow, self).__init__(parent)
        self.setupUi(self)
        self.setupModels()
        self.faceName = ""

    def setupModels(self):
        self.faceModel = FaceModel(self)
        self.faceModel.init()
        self.faceView.setModel(self.faceModel)
        self.faceView.smileyClicked.connect(self.returnSmileyName)

    def returnSmileyName(self, faceName):
        self.faceName = "[%s]" % faceName
        self.done(True)