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
        threading.Thread.__init__(self)
        self.sleep_time = sleep_time
        self.run_function = run_function
        # 外部需要停止该线程时触发事件
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            self.stop_event.wait(self.sleep_time)
            #self.run_function()
