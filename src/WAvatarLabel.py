from PyQt4 import QtCore, QtGui
from WAsyncLabel import WAsyncLabel


class WAvatarLabel(WAsyncLabel):

    NO_VERIFY = 0
    PERSONAL_VERIFY = 1
    ORGANIZATION_VERIFY = 2

    def __init__(self, verify_type, reason="", parent=None):
        super(WAvatarLabel, self).__init__(parent)
        self.__verity_type = verify_type
        self.setToolTip(reason)

    def _setPixmap(self, path):
        super(WAvatarLabel, self)._setPixmap(path)

        if self.__verity_type == self.NO_VERIFY:
            return
        elif self.__verity_type == self.PERSONAL_VERIFY:
            newPixmap = self.__draw_verify_icon(self._image, QtGui.QPixmap(":/IMG/img/verify_personal.png"))
        elif self.__verity_type == self.ORGANIZATION_VERIFY:
            newPixmap = self.__draw_verify_icon(self._image, QtGui.QPixmap(":/IMG/img/verify_organization.png"))
        super(WAsyncLabel, self).setPixmap(newPixmap)

    def __draw_verify_icon(self, pixmap, verify_pixmap):
        newPixmap = pixmap.copy()
        verify_pixmap = verify_pixmap.scaledToHeight(20, QtCore.Qt.SmoothTransformation)
        painter = QtGui.QPainter()
        painter.begin(newPixmap)
        painter.drawPixmap(self._image.height() - verify_pixmap.height(),
                           self._image.width() - verify_pixmap.width(),
                           verify_pixmap)
        painter.end()
        return newPixmap
