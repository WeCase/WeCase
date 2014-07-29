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
        with open(self._path, "a+") as f:
            f.seek(0)
            lines = f.readlines()

        with open(self._path, "w") as f:
            for line in lines:
                line = line[:-1]  # \n
                account, pid = line.split(" ")[0:2]
                pid = int(pid)

                if pid_running(pid):
                    yield f, account, pid

    @property
    def accounts(self):
        accounts = []

        for f, account, pid in self._open():
            f.write("%s %d\n" % (account, pid))
            accounts.append(account)
        return accounts

    def add_account(self, account):
        with open(self._path, "a+") as f:
            f.write("%s %d\n" % (account, os.getpid()))

    def remove_account(self, account_to_remove):
        for f, account, pid in self._open():
            if account == account_to_remove:
                continue
            f.write("%s %d\n" % (account, pid))
