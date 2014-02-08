#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented
#           "The Hackable Utils Library" - many useful small functions.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from threading import Thread
import sys
import os
import platform
import webbrowser


def workaround_excepthook_bug():
    # HACK: Python Exception Hook doesn't work in other threads.
    # There is a workaround.
    # See: http://bugs.python.org/issue1230540
    init_old = Thread.__init__

    # insert dirty hack
    def init(self, *args, **kwargs):
        init_old(self, *args, **kwargs)
        run_old = self.run

        def run_with_except_hook(*args, **kw):
            try:
                run_old(*args, **kw)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info())

        self.run = run_with_except_hook

    # Monkey patching Thread
    Thread.__init__ = init


def async(func):
    def exec_thread(*args):
        return Thread(group=None, target=func, args=args).start()
    return exec_thread


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonDecorator():

    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


@async
def start(filename):
    if platform.system() == "Linux":
        os.system('xdg-open "%s" > /dev/null' % filename)
    elif platform.system() == "Darwin":
        os.system('open "%s"' % filename)
    elif platform.system().startswith("CYGWIN"):
        os.system('cygstart "%s"' % filename)
    elif platform.system() == "Windows":
        os.system('start "" "%s"' % filename)
    else:
        assert False


def pid_running(pid):
    if platform.system() == "Windows":
        return _windows_pid_running(pid)
    else:
        try:
            return _unix_pid_running(pid)
        except Exception:
            assert False, "Unsupported platform."


def _windows_pid_running(pid):
    import ctypes
    kernel32 = ctypes.windll.kernel32
    SYNCHRONIZE = 0x100000

    process = kernel32.OpenProcess(SYNCHRONIZE, 0, pid)
    if process:
        kernel32.CloseHandle(process)
        return True
    else:
        return False


def _unix_pid_running(pid):
    try:
        # pretend to kill it
        os.kill(pid, 0)
    except OSError as e:
        # we don't have the permission to kill it, confirms the pid is exist.
        return e.errno == os.errno.EPERM
    return True


def getDirSize(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def clearDir(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except OSError:
            pass


def UNUSED(var):
    return var


def getGeometry(qWidget):
    return {"height": qWidget.height(),
            "width": qWidget.width(),
            "x": qWidget.x(),
            "y": qWidget.y()}


def setGeometry(qWidget, geometry_dic):
    width = geometry_dic.get("width")
    height = geometry_dic.get("height")
    if width and height:
        qWidget.resize(width, height)

    x = geometry_dic.get("x")
    y = geometry_dic.get("y")
    if x and y:
        qWidget.move(x, y)


def openLink(link):
    if not link:
        # not a link
        pass
    elif not "://" in link:
        # no protocol
        link = "http://" + link
        webbrowser.open(link)
    elif "http://" in link:
        webbrowser.open(link)
