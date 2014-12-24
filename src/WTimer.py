# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented a more flexible timer than QTimer.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from threading import Timer


class WTimer(Timer):

    def __init__(self, run_function, sleep_time, *args, **kwargs):
        super().__init__(sleep_time, run_function, args, kwargs)
        self.daemon = 1
        print("The use of WTimer is deprecated!")

    def run(self):
        super().run()
        self.finished.clear()

    def stop(self, join=False):
        super().cancel()
        if join:
            self.join()
