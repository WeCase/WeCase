#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented a LoginInfo() class to
#           avoid login a account more than once.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


import os
import tempfile
from WeHack import pid_running


class LoginInfo():

    FILENAME = "WeCase_ec7a4ecb-696a-41df-8b72-c2d25ce215ec"

    def __init__(self):
        self._path = "/".join((tempfile.gettempdir(), self.FILENAME))

    def _open(self):
        # a+ in Python has a different behavior from POSIX (the man page of fopen),
        # initial file position for reading is at EOF instead of BOF.
        return open(self._path, "a+")

    @property
    def accounts(self):
        accounts = []

        with self._open() as f:
            f.seek(0)
            for line in f:
                line = line[:-1]  # \n
                account, pid = line.split(" ")
                if pid_running(int(pid)):
                    accounts.append(account)
        return accounts

    def add_account(self, account):
        with self._open() as f:
            f.write("%s %d\n" % (account, os.getpid()))
