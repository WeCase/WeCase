#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented AboutWindow.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtGui
import version
from AboutWindow_ui import Ui_About_Dialog


class AboutWindow(QtGui.QDialog, Ui_About_Dialog):

    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)

    def _setPkgProvider(self):
        if version.pkgprovider == version.default_provider:
            vanilla = self.tr("Vanilla Version")
            self.distLabel.setText(vanilla)
        else:
            disttext = version.pkgprovider
            self.distLabel.setText(self.distLabel.text() % disttext)

    def _setVersionLabel(self):
        self.versionLabel.setText(self.versionLabel.text() % version.pkgversion)

    def _setDescriptionLabel(self):
        self.descriptionLabel.setText(self.descriptionLabel.text() % version.bug_report_url)

    def setupUi(self, widget):
        super().setupUi(widget)

        self._setPkgProvider()
        self._setVersionLabel()
        self._setDescriptionLabel()
