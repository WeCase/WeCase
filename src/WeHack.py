from threading import Thread
import os
import platform


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


@async
def start(filename):
    if platform.system() == "Linux":
        os.system("xdg-open %s > /dev/null" % filename)
    elif platform.system() == "Darwin":
        os.system("open %s" % filename)
    elif platform.system() == "Windows":
        os.system("start %s" % filename)
    else:
        assert False


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
