from PyQt4 import QtGui


class WImageLabel(QtGui.QLabel):

    def __init__(self, parent=None):
        super(WImageLabel, self).__init__(parent)

    def setImage(self, path):
        self._movie = QtGui.QMovie(path)
        self.setMovie(self._movie)
        self.start()

    def start(self):
        self._movie.start()

    def stop(self):
        self._movie.stop()



