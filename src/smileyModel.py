#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented a model for smileies 
# Copyright: GPL v3 or later.

from PyQt4 import QtCore

class smileyModel(QtCore.QAbstractListModel):
    nameRole = QtCore.Qt.UserRole + 1
    pathRole = QtCore.Qt.UserRole + 2

    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.setRoleNames()
        self.smileies = {}

    def roleNames(self):
        names = {}
        names[self.nameRole] = "name"
        nanes[self.pathRole] = "path"
        return names

    def data(self, role):
        if role == self.nameRole:
            return self.smileies["name"]
        elif role == self.pathRole:
            return self.smileies["path"]
        else:
            return None
