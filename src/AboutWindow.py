#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented AboutWindow.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


from PyQt4 import QtGui
from AboutWindow_ui import Ui_About_Dialog


class AboutWindow(QtGui.QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
