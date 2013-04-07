#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented a model for smileies 
# Copyright: GPL v3 or later.

from PyQt4 import QtCore

class SmileyItem(QtCore.QAbstractItemModel):
    def __init__(self, name, path, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.name = name
        self.path = path
        print("name: %s, path: %s" % (self.name, self.path))


class SmileyModel(QtCore.QAbstractListModel):
    nameRole = QtCore.Qt.UserRole + 1
    pathRole = QtCore.Qt.UserRole + 2

    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.setRoleNames(self.roleNames())
        self.smileies = []

    def appendRow(self, item):
        self.insertRow(self.rowCount(), item)

    def insertRow(self, row, item):
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.smileies.insert(row, item)
        self.endInsertRows()

    def roleNames(self):
        names = {}
        names[self.nameRole] = "name"
        names[self.pathRole] = "path"
        return names

    def data(self, index, role):
        if role == self.nameRole:
            return self.smileies[index.row()].name
        elif role == self.pathRole:
            return self.smileies[index.row()].path
        else:
            return None

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.smileies)
