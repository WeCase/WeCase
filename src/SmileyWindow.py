#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented SmileyWindow.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui
from Smiley import SmileyModel, SmileyItem
from SmileyWindow_ui import Ui_SmileyWindow
import const


class SmileyWindow(QtGui.QDialog, Ui_SmileyWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setupModels()
        self.smileyName = ""

    def setupModels(self):
        self.smileyModel = SmileyModel(self)
        self.smileyModel.init_smileies(const.myself_path + "./ui/img/smiley",
                                       self.smileyModel, SmileyItem)
        self.smileyView.setModel(self.smileyModel)
        self.smileyView.smileyClicked.connect(self.returnSmileyName)

    def returnSmileyName(self, smileyName):
        self.smileyName = "[%s]" % smileyName
        self.done(True)
