#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client, Since 4th, Feb, 2013.
#           This is the main file of WeCase.
# Copyright: GPL v3 or later.


import sys
import os
from PyQt4 import QtCore, QtGui
from LoginWindow import LoginWindow
import path
import traceback
import signal
import logging
import WeHack


WeHack.UNUSED(None)


def mkconfig():
    try:
        os.makedirs(path.config_path.replace("/config_db", ""))
    except OSError:
        pass

    try:
        os.makedirs(path.cache_path)
    except OSError:
        pass


class ErrorWindow(QtCore.QObject):

    raiseException = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.raiseException.connect(self.showError)

    @QtCore.pyqtSlot(str)
    def showError(self, traceback):
        messageBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, self.tr("Unknown Error"), "")
        layout = messageBox.layout()
        if layout:
            textEdit = QtGui.QPlainTextEdit(traceback)
            textEdit.setReadOnly(True)
            textEdit.setFixedHeight(250)
            textEdit.setFixedWidth(600)
            layout.addWidget(textEdit, 0, 1)
        messageBox.exec()


def my_excepthook(type, value, tback):
    if "last_error" not in globals().keys():
        global last_error
        last_error = None

    exception = "".join(traceback.format_exception(type, value, tback))
    error_info = (App.translate("main", "Oops, there is an unexpected error,\n") +
                  App.translate("main", "Please report it at https://github.com/WeCase/WeCase/issues\n\n") +
                  "%s" % exception)

    if type != last_error:
        last_error = type
        logging.error(error_info)
        errorWindow.raiseException.emit(error_info)
    else:
        logging.error("Same error...")

    # Call the default handler
    sys.__excepthook__(type, value, tback)


def import_warning():
    try:
        import notify2
        import dbus
        from dbus.exceptions import DBusException
        notify2.init("WeCase")
    except ImportError:
        QtGui.QMessageBox.warning(
            None,
            App.translate("main", "Notification disabled"),
            App.translate("main", "dbus-python or notify2 is not found. Notification will disable."))
    except DBusException:
        QtGui.QMessageBox.warning(
            None,
            App.translate("main", "Notification disabled"),
            App.translate("main", "Notification Daemon not exist. Notification will disable."))


def setup_logger():
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %('
                               'message)s',
                        datefmt='%m-%d %H:%M',
                        filename=path.cache_path + "log")
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


if __name__ == "__main__":
    mkconfig()
    setup_logger()

    App = QtGui.QApplication(sys.argv)
    App.setApplicationName("WeCase")
    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec. codecForName("UTF-8"))

    # Exceptions may happen in other threads.
    # So, use signal/slot to avoid threads' issue.
    sys.excepthook = my_excepthook
    WeHack.workaround_excepthook_bug()
    errorWindow = ErrorWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Qt's built-in string translator
    qt_translator = QtCore.QTranslator(App)
    qt_translator.load("qt_" + QtCore.QLocale.system().name(),
                       QtCore.QLibraryInfo.location(
                           QtCore.QLibraryInfo.TranslationsPath))
    App.installTranslator(qt_translator)

    # WeCase's own string translator
    my_translator = QtCore.QTranslator(App)
    my_translator.load("WeCase_" + QtCore.QLocale.system().name(),
                       path.locale_path)
    App.installTranslator(my_translator)

    import_warning()
    wecase_login = LoginWindow()

    exit_status = App.exec_()

    # Cleanup code here.
    App.deleteLater()

    logging.info("Exited")
    sys.excepthook = sys.__excepthook__
    exit(exit_status)
