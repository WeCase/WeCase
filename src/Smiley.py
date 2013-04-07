#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented a model for smileies 
# Copyright: GPL v3 or later.

import os
from PyQt4 import QtCore

class SmileyItem(QtCore.QAbstractItemModel):
    def __init__(self, name, path, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.name = name
        self.path = path


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


def init_smileies(root, smiley_model, smiley_item):
    def walk(root):
        for file in os.listdir(root):
            path = os.path.join(root, file)
            if os.path.isdir(path):
                for file in walk(path):
                    yield file
            else:
                yield path

    def is_smiley(filename):
        filename = filename.split('.')
        if filename[-1] == "gif":
            return True
        else:
            return False

    for filepath in walk(root):
        filepath = os.path.abspath(filepath)
        filename = filepath.split('/')[-1]
        if is_smiley(filename):
            smiley_name = os.path.splitext(filepath)[0]
            file_content = open(smiley_name).read().replace('\n', '')
            smiley_model.appendRow(smiley_item(file_content, filepath.replace("./ui", "")))
