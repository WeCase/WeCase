from threading import Thread
import os
import platform

def async(func):
    def exec_thread(*args):
        return Thread(group=None, target=func, args=args).start()
    return exec_thread

def start(filename):
    if platform.system() == "Linux":
        os.system("xdg-open %s > /dev/null" % (filename))
    elif platform.system() == "Darwin":
        os.system("open %s" % (filename))
    elif platform.system() == "Windows":
        os.system("start %s" % (filename))
    else:
        assert False
