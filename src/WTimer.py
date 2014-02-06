#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client
# This file implemented a QTimer-like timer
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


from threading import Thread, Event


class WTimer(Thread):

    def __init__(self, run_function, sleep_time):
        super(WTimer, self).__init__()
        self.sleep_time = sleep_time
        self.run_function = run_function
        self._stop_event = Event()

    def run(self):
        while not self._stop_event.is_set():
            self._stop_event.wait(self.sleep_time)
            self.run_function()

    def stop(self, join=False):
        self._stop_event.set()
        if join:
            self.join()
