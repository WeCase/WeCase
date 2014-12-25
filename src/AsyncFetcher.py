# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented an Async File Downloader.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from PyQt4 import QtCore
import pycurl
from WeHack import async, SingletonDecorator
from threading import Event
import os
from time import sleep
import logging


class SignalSender(QtCore.QObject):

    fetched = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(SignalSender, self).__init__(parent)

    def emit(self, target):
        self.fetched.emit(target)

    def connect(self, target):
        self.fetched.connect(target)

    def disconnect(self, target):
        self.fetched.disconnect(target)


class _AsyncFetcher(QtCore.QObject):

    DO_NOT_HAVE = 0
    DOWNLOADED = 1
    DOWNLOADING = 2

    def __init__(self, path, parent=None):
        super(_AsyncFetcher, self).__init__(parent)

        if path[-1] != "/":
            # fix the non-standard path.
            path += "/"
            print("Warning: non-standard path")
        if not os.path.exists(path):
            os.makedirs(path)

        self.path = path
        self._signals = {}
        self._got_state = Event()

    @staticmethod
    def _formattedFilename(url):
        url_parts = url.split('/')
        return "%s_%s" % (url_parts[-2], url_parts[-1])

    @staticmethod
    def download(url, filepath):
        curl = pycurl.Curl()
        curl.setopt(pycurl.NOSIGNAL, True)  # thread-safe
        curl.setopt(pycurl.SSL_VERIFYHOST, 2)
        curl.setopt(pycurl.SSL_VERIFYPEER, True)
        curl.setopt(pycurl.ENCODING, "")  # accept all encodings
        curl.setopt(pycurl.HEADERFUNCTION, lambda x: None)  # disable stdout logging

        curl.setopt(pycurl.HTTPGET, 1)
        curl.setopt(pycurl.URL, url)

        with open(filepath, "wb") as file:
            curl.setopt(pycurl.WRITEFUNCTION, file.write)
            curl.perform()
            if curl.getinfo(pycurl.RESPONSE_CODE) != 200:
                raise IOError

    @async
    def _download(self, url, filepath):
        while 1:
            try:
                self.download(url, filepath)
                break
            except (IOError, pycurl.error):
                logging.warning("Downloading %s failed, retry..." % url)
                sleep(1)
                continue

        self._got_state.wait()
        self._process_callbacks(filepath)

    def _get_state(self, filepath):
        if self._signals.get(filepath, []):
            assert os.path.exists, "The file should exists, but it doesn't exist."
            return self.DOWNLOADING
        elif os.path.exists(filepath):
            return self.DOWNLOADED
        return self.DO_NOT_HAVE

    def _add_callback(self, filepath, callback):
        signal = SignalSender()
        signal.connect(callback)

        try:
            array = self._signals[filepath]
            array.append(signal)
        except KeyError:
            self._signals[filepath] = [signal]

    def _process_callbacks(self, filepath):
        signals = self._signals[filepath]
        for signal in signals:
            signal.emit(filepath)
        self._signals[filepath] = []

    def addTask(self, url, callback):
        filename = self._formattedFilename(url)
        filepath = "%s%s" % (self.path, filename)

        self._got_state.clear()

        state = self._get_state(filepath)
        self._add_callback(filepath, callback)
        if state == self.DO_NOT_HAVE:
            self._download(url, filepath)
        elif state == self.DOWNLOADING:
            pass
        elif state == self.DOWNLOADED:
            self._process_callbacks(filepath)
        else:
            assert False, "Downloaded but downloading now?"

        self._got_state.set()

AsyncFetcher = SingletonDecorator(_AsyncFetcher)
