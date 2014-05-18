#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented an Error handler for Sina's API.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui


class APIErrorWindow(QtCore.QObject):

    raiseException = QtCore.pyqtSignal(Exception)

    def __init__(self, parent=None):
        super(APIErrorWindow, self).__init__(parent)
        self.raiseException.connect(self.showAPIException)

        self.ERRORS = {
            20101: self.tr("This tweet have been deleted."),
            20704: self.tr("This tweet have been collected already."),
            20705: self.tr("This tweet doesn't in your collection."),
            20003: self.tr("User doesn't exists."),
            20006: self.tr("Image is too large."),
            20012: self.tr("Text is too long."),
            20016: self.tr("Your send too many tweets in a short time."),
            20019: self.tr("Don't send reperted tweet."),
            20018: self.tr("Your tweet contains illegal website."),
            20020: self.tr("Your tweet contains ads."),
            20021: self.tr("Your tweet contains illegal text."),
            20022: self.tr("Your IP address is in the blacklist."),
            20032: self.tr("Send successful, but your tweet won't display immediately, please wait for a minute."),
            20101: self.tr("The tweet does not exist."),
            20111: self.tr("Don't send reperted tweet."),
            21335: self.tr("The API was banned by Sina. I can't fetch any timeline except yours.")
        }

    @QtCore.pyqtSlot(Exception)
    def showAPIException(self, exception):
        try:
            error_message = self.ERRORS[int(exception.error_code)]
        except KeyError:
            error_message = "%d: %s" % (int(exception.error_code), exception.error)
        QtGui.QMessageBox.warning(None, self.tr("Error"), error_message)
