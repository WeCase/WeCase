#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented Notify.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


from PyQt4 import QtCore
import path

try:
    import notify2 as pynotify
    from dbus.exceptions import DBusException
    pynotify.init("WeCase")
except ImportError:
    import nullNotify as pynotify
except DBusException:
    import nullNotify as pynotify


class Notify(QtCore.QObject):
    image = path.icon_path

    def __init__(self, appname=QtCore.QObject().tr("WeCase"), timeout=5):
        super(Notify, self).__init__()

        pynotify.init(appname)
        self.timeout = timeout
        self.n = pynotify.Notification(appname)

    def showMessage(self, title, text):
        try:
            self.n.update(title, text, self.image)
            self.n.set_timeout(self.timeout * 1000)
            self.n.show()
        except DBusException:
            return False
        return True
