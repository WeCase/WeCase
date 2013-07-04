from PyQt4 import QtCore, QtGui


class WTweetLabel(QtGui.QTextBrowser):

    def __init__(self, text, parent=None):
        super(WTweetLabel, self).__init__(parent)
        self.setReadOnly(True)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Base, QtCore.Qt.transparent)
        self.setPalette(pal)

        self.setOpenExternalLinks(True)
        self.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.connect(self.document().documentLayout(),
                     QtCore.SIGNAL("documentSizeChanged(QSizeF)"),
                     QtCore.SLOT("adjustMinimumSize(QSizeF)"))

    @QtCore.pyqtSlot(QtCore.QSizeF)
    def adjustMinimumSize(self, size):
        self.setMinimumHeight(size.height() + 2 * self.frameWidth())
