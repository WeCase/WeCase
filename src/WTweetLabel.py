from PyQt4 import QtCore, QtGui
import webbrowser


class WTweetLabel(QtGui.QTextBrowser):

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
        _url = url
        url = url.toString()
        print(_url.toString(), _url.toEncoded())

        if not "://" in url:
            # no protocol
            url = "http://" + url
            webbrowser.open(url)
        elif "http://" in url:
            webbrowser.open(url)
        elif "mentions://" in url:
            print("Clicked user %s" % url[12:])
        elif "hashtag://" in url:
            print("Clicked a tag %s" % url[11:])
