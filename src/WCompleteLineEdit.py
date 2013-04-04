#!/usr/bin/python
import threading
from PyQt4 import QtGui, QtCore


class WCompleteLineEdit(QtGui.QTextEdit):
    callbackFinished = QtCore.pyqtSignal(list)

    def __init__(self, parent=None, words=None, callback=None):
        QtGui.QTextEdit.__init__(self)
        self.separator = ' '
        self.mention_flag = None
        self.mention = False
        self.words_callback = callback
        self.words = words

        self.listView = QtGui.QListView(self)
        self.model = QtGui.QStringListModel(self)
        self.listView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listView.setWindowFlags(QtCore.Qt.ToolTip)
        self.setLineWrapMode(self.WidgetWidth)

    def setText(self, text, noSave=False):
        if not noSave:
            self.text = text
        super(WCompleteLineEdit, self).setText(text)

    def setupSignals(self):
        self.textChanged.connect(self.mentionStates)
        self.textChanged.connect(self.setCompleter)
        self.listView.clicked.connect(self.mouseCompleteText)
        self.callbackFinished.connect(self.showCompleter)

    def guessLength(self):
        # XXX: 迫不得已的恶心方法，见
        # http://stackoverflow.com/questions/15814776/
        # how-do-i-get-the-actual-visible-cursors-line-number
        text = ""
        while self.textCursor().columnNumber() == self.textCursor().position():
            text += "a"
            self.setText(text, True)
            self.moveCursorToEnd()
        self.line_max = self.textCursor().position()
        self.setText(self.text)

    def getLines(self):
        return self.textCursor().position() // self.line_max + 1

    def getNewText(self, original_text, new_text):
        original_text = original_text.split(self.separator)
        new_text = new_text.split(self.separator)
        original_text[-1] = new_text[-1]
        return self.separator.join(original_text) + self.separator

    def moveCursorToEnd(self):
        cursor = QtGui.QTextCursor(self.textCursor())
        cursor.movePosition(QtGui.QTextCursor.EndOfBlock)
        self.setTextCursor(cursor)

    def focusOutEvent(self, event):
        self.listView.hide()

    def focusInEvent(self, event):
        self.guessLength()
        self.setupSignals()

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
                #  退出菜单
                self.listView.hide()

            elif key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                # 补全单词
                if currentIndex.isValid():
                    text = self.getNewText(self.toPlainText(),
                            self.listView.currentIndex().data())
                    self.setText(text)
                    self.moveCursorToEnd()
                self.listView.hide()

            else:
                # 什么都不做，调用父类 LineEdit 的按键事件
                self.listView.hide()
                super(WCompleteLineEdit, self).keyPressEvent(event)
        else:
            super(WCompleteLineEdit, self).keyPressEvent(event)

    def mentionStates(self):
        text = self.toPlainText()
        if not self.mention_flag:
            return True
        if not text:
            self.mention = False
        if text and (text[-1] == self.mention_flag):
            self.mention = True
        elif text and (text[-1] == self.separator):
            self.mention = False

    def setCompleter(self):
        text = self.toPlainText()
        text = text.split(self.separator)[-1]

        if not text:
            self.listView.hide()
            return
        if not self.words and not self.words_callback:
            return
        if not self.mention:
            return
        if (len(text) > 1) and (not self.listView.isHidden()):
            return

        if self.words_callback:
            threading.Thread(group=None, target=self.runCallback).start()
            self.showCompleter(["Loading..."])
            return
        else:
            sl = []
            for word in self.words:
                if text in word:
                    sl.append(word)

        self.showCompleter(sl)

    def runCallback(self):
        text = self.toPlainText()
        text = text.split(self.separator)[-1]
        lst = self.words_callback(text)
        self.callbackFinished.emit(lst)

    def showCompleter(self, lst):
        self.listView.hide()
        self.model.setStringList(lst)
        self.listView.setModel(self.model)

        if self.model.rowCount() == 0:
            return

        self.listView.setMinimumWidth(self.width())
        self.listView.setMaximumWidth(self.width())
        p = QtCore.QPoint(0, self.cursorRect().height() * 1.5 * self.getLines())
        x = self.mapToGlobal(p).x()
        y = self.mapToGlobal(p).y()
        self.listView.move(x, y)
        self.listView.show()

    def mouseCompleteText(self, index):
        text = self.getNewText(self.toPlainText(), index.data())
        self.setText(text)
        self.moveCursorToEnd()
        self.listView.hide()
