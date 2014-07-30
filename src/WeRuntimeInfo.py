# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented a dict wrapper allowing to save and read
#           the global shared data.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from WeHack import Singleton


class WeRuntimeInfo(dict, metaclass=Singleton):
    def __init__(self, *args):
        dict.__init__(self, args)
