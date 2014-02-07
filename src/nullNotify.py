#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented a dummy notification interface for
#           unsupperted platforms.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from WeHack import UNUSED


def init(*args):
    UNUSED(args)
    return True


class Notification():
    def __init__(self, *args):
        pass

    def update(self, *args):
        pass

    def set_timeout(self, *args):
        pass

    def show(self):
        pass
