#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented LoginWindow.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


import webbrowser
from WeHack import async
from weibos.helper import SUCCESS, PASSWORD_ERROR, NETWORK_ERROR, UBAuthorize
from PyQt4 import QtCore, QtGui
from LoginWindow_ui import Ui_frm_Login
from WeCaseWindow import WeCaseWindow
import path
from time import sleep
from WConfigParser import WConfigParser
from LoginInfo import LoginInfo


class LoginWindow(QtGui.QDialog, Ui_frm_Login):

    SUCCESS = SUCCESS
    PASSWORD_ERROR = PASSWORD_ERROR
    NETWORK_ERROR = NETWORK_ERROR
    LOGIN_ALREADY = 10

    loginReturn = QtCore.pyqtSignal(int)

    def __init__(self, allow_auto_login=True, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.allow_auto_login = allow_auto_login
        self.loadConfig()
        self.setupUi(self)
        self.setupSignals()
        self.err_count = 0

    def setupSignals(self):
        # Other signals defined in Designer.
        self.loginReturn.connect(self.checkLogin)
        self.chk_Remember.clicked.connect(self.uncheckAutoLogin)

    def accept(self):
        if self.chk_Remember.isChecked():
            self.passwd[str(self.username)] = str(self.password)
            self.last_login = str(self.username)
            # Because this is a model dialog,
            # closeEvent won't emit when we accept() the window, but will
            # emit when we reject() the window.
            self.saveConfig()
            self.setParent(None)
        wecase_main = WeCaseWindow()
        wecase_main.show()
        # Maybe users will logout, so reset the status
        LoginInfo().add_account(self.username)
        self.pushButton_log.setText(self.tr("GO!"))
        self.pushButton_log.setEnabled(True)
        self.done(True)

    def reject(self, status):
        if status in (self.NETWORK_ERROR, self.PASSWORD_ERROR) and self.err_count < 5:
            self.err_count += 1
            sleep(0.5)
            self.ui_authorize()
            return
        elif status == self.PASSWORD_ERROR:
            QtGui.QMessageBox.critical(None, self.tr("Authorize Failed!"),
                                       self.tr("Check your account and password"))
            self.err_count = 0
        elif status == self.NETWORK_ERROR:
            QtGui.QMessageBox.critical(None, self.tr("Network Error"),
                                       self.tr("Something wrong with the network, please try again."))
            self.err_count = 0
        elif status == self.LOGIN_ALREADY:
            QtGui.QMessageBox.critical(None, self.tr("Already Logged in"),
                                       self.tr("This account is already logged in."))

        self.pushButton_log.setText(self.tr("GO!"))
        self.pushButton_log.setEnabled(True)

    def checkLogin(self, status):
        if status == self.SUCCESS:
            self.accept()
        else:
            self.reject(status)

    def setupUi(self, widget):
        super(LoginWindow, self).setupUi(widget)
        self.show()
        self.txt_Password.setEchoMode(QtGui.QLineEdit.Password)
        self.cmb_Users.lineEdit().setPlaceholderText(self.tr("ID/Email/Phone"))
        self.cmb_Users.addItem(self.last_login)

        for username in list(self.passwd.keys()):
            if username == self.last_login:
                continue
            self.cmb_Users.addItem(username)

        if self.cmb_Users.currentText():
            self.chk_Remember.setChecked(True)
            self.setPassword(self.cmb_Users.currentText())

        if self.auto_login:
            self.chk_AutoLogin.setChecked(self.auto_login)
            self.login()

    def loadConfig(self):
        self.login_config = WConfigParser(path.myself_path + "WMetaConfig",
                                          path.config_path, "login")
        self.passwd = self.login_config.passwd
        self.last_login = self.login_config.last_login
        self.auto_login = self.login_config.auto_login and self.allow_auto_login

    def saveConfig(self):
        self.login_config.passwd = self.passwd
        self.login_config.last_login = self.last_login
        self.login_config.auto_login = self.chk_AutoLogin.isChecked()
        self.login_config.save()

    def login(self):
        self.pushButton_log.setText(self.tr("Login, waiting..."))
        self.pushButton_log.setEnabled(False)
        self.ui_authorize()

    def ui_authorize(self):
        self.username = self.cmb_Users.currentText()
        self.password = self.txt_Password.text()
        self.authorize(self.username, self.password)

    @async
    def authorize(self, username, password):
        if username in LoginInfo().accounts:
            self.loginReturn.emit(self.LOGIN_ALREADY)
            return

        result = UBAuthorize(username, password)
        if result == SUCCESS:
            self.loginReturn.emit(self.SUCCESS)
        elif result == PASSWORD_ERROR:
            self.loginReturn.emit(self.PASSWORD_ERROR)
        elif result == NETWORK_ERROR:
            self.loginReturn.emit(self.NETWORK_ERROR)

    def setPassword(self, username):
        if username in self.passwd.keys():
            self.txt_Password.setText(self.passwd[username])

    @QtCore.pyqtSlot(bool)
    def uncheckAutoLogin(self, checked):
        if not checked:
            self.chk_AutoLogin.setChecked(False)

    def openRegisterPage(self):
        webbrowser.open("http://weibo.com/signup/signup.php")

    def closeEvent(self, event):
        # HACK: When a user want to close this window, closeEvent will emit.
        # But if we don't have closeEvent, Qt will call reject(). We use
        # reject() to show the error message, so users will see the error and
        # they can not close this window. So just do nothing there to allow
        # users to close the window.
        pass
