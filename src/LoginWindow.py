#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented LoginWindow.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import webbrowser
from WeHack import async
from weibo import APIClient
from PyQt4 import QtCore, QtGui
from LoginWindow_ui import Ui_frm_Login
from WeCaseWindow import WeCaseWindow
import const
from TweetUtils import authorize
from time import sleep
from WeCaseConfig import WeCaseConfig


class LoginWindow(QtGui.QDialog, Ui_frm_Login):
    SUCCESS = 0
    PASSWORD_ERROR = 1
    NETWORK_ERROR = 2
    loginReturn = QtCore.pyqtSignal(int)

    def __init__(self, allow_auto_login=True, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.allow_auto_login = allow_auto_login
        self.loadConfig()
        self.setupUi(self)
        self.setupSignals()
        self.net_err_count = 0

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
        wecase_main = WeCaseWindow()
        wecase_main.show()
        # Maybe users will logout, so reset the status
        self.pushButton_log.setText(self.tr("GO!"))
        self.pushButton_log.setEnabled(True)
        self.done(True)

    def reject(self, status):
        if status == self.PASSWORD_ERROR:
            QtGui.QMessageBox.critical(None, self.tr("Authorize Failed!"),
                                       self.tr("Check your account and password"))
        elif status == self.NETWORK_ERROR and self.net_err_count < 3:
            self.net_err_count += 1
            sleep(0.5)
            self.ui_authorize()
            return
        elif status == self.NETWORK_ERROR and self.net_err_count == 3:
            QtGui.QMessageBox.critical(None, self.tr("Network Error"),
                                       self.tr("Something wrong with the network, please try again."))
            self.net_err_count = 0

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
        self.login_config = WeCaseConfig(const.config_path, "login")
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
        try:
            client = APIClient(app_key=const.APP_KEY, app_secret=const.APP_SECRET,
                               redirect_uri=const.CALLBACK_URL)

            # Step 1: Get the authorize url from Sina
            authorize_url = client.get_authorize_url()

            # Step 2: Send the authorize info to Sina and get the authorize_code
            authorize_code = authorize(authorize_url, username, password)
            if not authorize_code:
                self.loginReturn.emit(self.PASSWORD_ERROR)

            # Step 3: Get the access token by authorize_code
            r = client.request_access_token(authorize_code)

            # Step 4: Setup the access token of SDK
            client.set_access_token(r.access_token, r.expires_in)
            const.client = client
            self.loginReturn.emit(self.SUCCESS)
        except:
            self.loginReturn.emit(self.NETWORK_ERROR)

    def setPassword(self, username):
        if username:
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
