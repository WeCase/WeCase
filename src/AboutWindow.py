#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented AboutWindow.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


from PyQt4 import QtGui
import version
from AboutWindow_ui import Ui_About_Dialog


class AboutWindow(QtGui.QDialog, Ui_About_Dialog):

    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, widget):
        super().setupUi(widget)

        if version.pkgprovider == version.default_provider:
            vanilla = self.tr("Vanilla Version")
            widget.distLabel.setText(vanilla)
        else:
            disttext = version.pkgprovider
            widget.distLabel.setText(widget.distLabel.text() % disttext)

        widget.versionLabel.setText(widget.versionLabel.text() % version.pkgversion)
        widget.descriptionLabel.setText(widget.descriptionLabel.text() % version.bug_report_url)
