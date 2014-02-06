from PyQt4 import QtCore, QtGui
from copy import copy


# WARNING: This is the most ugly part of WeCase


class ComboBoxDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        return editor

    def setEditorData(self, editor, index):
        optionsDict = index.data(FilterTableModel.OptionRole)
        if index.column() == FilterTableModel.TYPE:
            options = list(optionsDict.keys())
        elif index.column() == FilterTableModel.ACTION:
            type = index.sibling(index.row(), FilterTableModel.TYPE).data(QtCore.Qt.DisplayRole)
            if type:
                options = optionsDict[type]
            else:
                options = []
        editor.addItems(options)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), QtCore.Qt.EditRole)

        if index.column() == FilterTableModel.TYPE:
            optionsDict = index.data(FilterTableModel.OptionRole)
            type = index.sibling(index.row(), FilterTableModel.TYPE).data(QtCore.Qt.DisplayRole)
            if index.sibling(index.row(), FilterTableModel.ACTION).data(QtCore.Qt.DisplayRole) not in optionsDict[type]:
                model.setData(index.sibling(index.row(), FilterTableModel.ACTION), None, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class FilterTableModel(QtCore.QAbstractTableModel):

    OptionRole = QtCore.Qt.UserRole
    TYPE = 0
    VALUE = 1
    ACTION = 2

    def __init__(self, parent=None, rows=1, cols=3):
        super(FilterTableModel, self).__init__(parent)
        self._data = []
        self._default_cols = cols

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        try:
            return len(self._data[0])
        except IndexError:
            return self._default_cols

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        elif role == self.OptionRole:
            return {self.tr("Keyword"): (self.tr("Block"), self.tr("Word War")),
                    self.tr("User"): (self.tr("Block"),)}

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False

        self._data[index.row()][index.column()] = value
        self.dataChanged.emit(index, index)
        # don't forget to cast
        return True

    def headerData(self, section, orientatidon, role):
        if orientatidon == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return (self.tr("Type"), self.tr("Value"), self.tr("Action"))[section]

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        assert 0 <= row <= self.rowCount()
        assert count > 0

        self.beginInsertRows(parent, row, row + count - 1)
        new_row = [None] * self.columnCount()
        for row in range(row, row + count):
            self._data.insert(row, copy(new_row))
        self.endInsertRows()

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        assert 0 <= row <= self.rowCount()
        assert count > 0

        self.beginRemoveRows(parent, row, row + count - 1)
        for row in range(row, row + count):
            del self._data[row]
        self.endRemoveRows()

    def insertColumns(self, col, count, parent=QtCore.QModelIndex()):
        assert 0 <= col <= self.columnCount()
        assert count > 0

        self.beginInsertColumns(parent, col, col + count - 1)
        for col in range(col, col + count):
            for _col in self._data:
                _col.insert(col, None)
        self.endInsertColumns()

    def _dump(self, type, action):
        blacklist = []

        for row in self._data:
            if row[self.TYPE] == type and row[self.VALUE] and row[self.ACTION] == action:
                blacklist.append(row[self.VALUE])
        return blacklist

    def _load(self, type, action, values):
        assert len(values) >= 0

        if len(values) == 0:
            return

        # found out the first blank line
        free = 0
        try:
            while self._data[free][self.TYPE]:
                free += 1
        except IndexError:
            # no blank line, create the first one by ourself.
            self.insertRows(self.rowCount(), 1)

        # create more blank lines, exclude the blank line which we already have
        if len(values) - 1 > 0:
            self.insertRows(free, len(values) - 1)

        # fill in these blank lines
        for value in values:
            self.setData(self.index(free, self.TYPE), type)
            self.setData(self.index(free, self.VALUE), value)
            self.setData(self.index(free, self.ACTION), action)
            free += 1

    def loadKeywordsBlacklist(self, blacklist):
        self._load(self.tr("Keyword"), self.tr("Block"), blacklist)

    def dumpKeywordsBlacklist(self):
        return self._dump(self.tr("Keyword"), self.tr("Block"))

    def loadUsersBlacklist(self, blacklist):
        self._load(self.tr("User"), self.tr("Block"), blacklist)

    def dumpUsersBlacklist(self):
        return self._dump(self.tr("User"), self.tr("Block"))

    def loadWordWarKeywords(self, keywords):
        self._load(self.tr("Keyword"), self.tr("Word War"), keywords)

    def dumpWordWarKeywords(self):
        return self._dump(self.tr("Keyword"), self.tr("Word War"))


class FilterTable(QtGui.QTableView):

    def __init__(self, parent=None):
        super(FilterTable, self).__init__(parent)
        self.setItemDelegateForColumn(0, ComboBoxDelegate(self))
        self.setItemDelegateForColumn(2, ComboBoxDelegate(self))
