from PyQt4 import QtCore, QtGui


class WImageLabel(QtGui.QLabel):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(WImageLabel, self).__init__(parent)

    def setImageFile(self, path):
        self.setMovie(QtGui.QMovie(path))

    def setMovie(self, movie):
        super(WImageLabel, self).setMovie(movie)
        movie.start()

    def start(self):
        self.movie().start()

    def stop(self):
        self.movie().stop()

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()