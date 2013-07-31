from PyQt4 import QtCore, QtGui
import webbrowser
import logging


class WTweetLabel(QtGui.QTextBrowser):

    userClicked = QtCore.pyqtSignal(str)
    tagClicked = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(WTweetLabel, self).__init__(parent)
        self.setReadOnly(True)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Base, QtCore.Qt.transparent)
        self.setPalette(pal)

        self.setOpenLinks(False)
        self.setOpenExternalLinks(False)
        self.anchorClicked.connect(self.openLink)
        self.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.connect(self.document().documentLayout(),
                     QtCore.SIGNAL("documentSizeChanged(QSizeF)"),
                     QtCore.SLOT("adjustMinimumSize(QSizeF)"))

    @QtCore.pyqtSlot(QtCore.QSizeF)
    def adjustMinimumSize(self, size):
        self.setMinimumHeight(size.height() + 2 * self.frameWidth())

    def openLink(self, url):
        url = url.toString()

        if not "://" in url:
            # no protocol
            url = "http://" + url
            webbrowser.open(url)
        elif "http://" in url:
            webbrowser.open(url)
        elif "mentions://" in url:
            self.userClicked.emit(url[13:])
        elif "hashtag://" in url:
            self.tagClicked.emit(url[11:])
