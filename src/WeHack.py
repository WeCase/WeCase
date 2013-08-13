from threading import Thread
import sys
import os
import platform


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


@async
def start(filename):
    if platform.system() == "Linux":
        os.system('xdg-open "%s" > /dev/null' % filename)
    elif platform.system() == "Darwin":
        os.system('open "%s"' % filename)
    elif platform.system() == "Windows":
        os.system('start "" "%s"' % filename)
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
