#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client
# This file implemented a QTimer-like timer
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import time
import threading

class WTimer(threading.Thread):
    def __init__(self, sleep_time, run_function):
    #def __init__(self):
        threading.Thread.__init__(self)
        self.stopped = False
        self.sleep_time = sleep_time
        self.run_function = run_function

    def run(self):
        while not self.stopped:
            time.sleep(self.sleep_time)
            self.run_function()
