#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented a general QTextEdit
#           with flexible auto-complete.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtGui, QtCore
from WeHack import async


class WAbstractCompleteLineEdit(QtGui.QTextEdit):
    fetchListFinished = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(WAbstractCompleteLineEdit, self).__init__(parent)
        self.cursor = self.textCursor()

        self.setupUi()
        self.setupSignals()

    def setupUi(self):
        self.listView = QtGui.QListView(self)
        self.model = QtGui.QStringListModel(self)
        self.listView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listView.setWindowFlags(QtCore.Qt.ToolTip)
        self.setLineWrapMode(self.WidgetWidth)

    def setupSignals(self):
        self.textChanged.connect(self.needComplete)
        self.textChanged.connect(self.setCompleter)
        self.listView.clicked.connect(self.mouseCompleteText)
        self.fetchListFinished.connect(self.showCompleter)

    def getLine(self):
        # 获得折行后屏幕上实际的行数
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)

        lines = 1
        while cursor.positionInBlock() > 0:
            cursor.movePosition(QtGui.QTextCursor.Up)
            lines += 1
        block = cursor.block().previous()

        while block.isValid():
            lines += block.lineCount()
            block = block.previous()
        return lines

    def getCompleteList(self):
        raise NotImplementedError

    def getNewText(self, original_text, new_text):
        raise NotImplementedError

    def focusOutEvent(self, event):
        self.listView.hide()

    def selectedText(self):
        self.cursor.setPosition(0)
        self.cursor.setPosition(self.textCursor().position(), QtGui.QTextCursor.KeepAnchor)
        return self.cursor.selectedText()

    def keyPressEvent(self, event):
        if not self.listView.isHidden():
            key = event.key()
            rowCount = self.listView.model().rowCount()
            currentIndex = self.listView.currentIndex()

            if key == QtCore.Qt.Key_Down:
                # 向下移动列表，越界回到顶部
                row = (currentIndex.row() + 1) % rowCount
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)

            elif key == QtCore.Qt.Key_Up:
                # 向上移动列表，越界回到底部
                row = (currentIndex.row() - 1) % rowCount
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)

            elif key == QtCore.Qt.Key_Escape:
                # 退出菜单
                self.listView.hide()

            elif key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                # 补全单词
                if currentIndex.isValid():
                    text = self.getNewText(
                        self.cursor.selectedText(),
                        self.listView.currentIndex().data())
                    self.cursor.insertText(text)
                self.textChanged.emit()
                self.listView.hide()

            else:
                # 什么都不做，调用父类 LineEdit 的按键事件
                self.listView.hide()
                super(WAbstractCompleteLineEdit, self).keyPressEvent(event)
        else:
            super(WAbstractCompleteLineEdit, self).keyPressEvent(event)

    def needComplete(self):
        raise NotImplementedError

    def setCompleter(self):
        text = self.selectedText()
        text = text.split(self.separator)[-1]

        if not text:
            self.listView.hide()
            return
        if not self.needComplete():
            return
        if (len(text) > 1) and (not self.listView.isHidden()):
            return

        self.getCompleteList()
        self.showCompleter(["Loading..."])

    def showCompleter(self, lst):
        self.listView.hide()
        self.model.setStringList(lst)
        self.listView.setModel(self.model)

        if self.model.rowCount() == 0:
            return

        self.listView.setMinimumWidth(self.width())
        self.listView.setMaximumWidth(self.width())

        # 10 是一个幻数，它不因字体大小的改变而改变，代表弹框与当前行的间隔
        p = QtCore.QPoint(0, self.cursorRect().height() * self.getLine() + 10)
        x = self.mapToGlobal(p).x()
        y = self.mapToGlobal(p).y()
        self.listView.move(x, y)
        self.listView.show()

    def mouseCompleteText(self, index):
        text = self.getNewText(self.selectedText(), index.data())
        self.cursor.insertText(text)
        self.textChanged.emit()
        self.listView.hide()


class WCompleteLineEdit(WAbstractCompleteLineEdit):
    mentionFlag = "@"
    separator = " "

    def __init__(self, parent):
        super(WCompleteLineEdit, self).__init__(parent)
        self._needComplete = False
        self.callback = None
        self.setAcceptRichText(False)  # 禁用富文本，微博很穷的

    @async
    def getCompleteList(self):
        result = self.callback(self.cursor.selectedText())
        self.fetchListFinished.emit(result)

    def getNewText(self, original_text, new_text):
        for index, value in enumerate(original_text):
            if value == self.mentionFlag:
                pos = index
        return original_text[:pos] + new_text + self.separator

    def needComplete(self):
        if not self.selectedText():
            return False
        elif self.selectedText()[-1] == self.mentionFlag:
            self._needComplete = True
            return self._needComplete
        elif self.selectedText()[-1] == self.separator:
            self._needComplete = False
            return self._needComplete
        else:
            return self._needComplete
