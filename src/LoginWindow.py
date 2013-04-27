#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented LoginWindow.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import webbrowser
import urllib.request
import urllib.parse
import urllib.error
import http.client
from configparser import ConfigParser
import threading
from weibo import APIClient
from PyQt4 import QtCore, QtGui
from LoginWindow_ui import Ui_frm_Login
from WeCaseWindow import WeCaseWindow
import const


class LoginWindow(QtGui.QDialog, Ui_frm_Login):
    loginReturn = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.loadConfig()
        self.setupUi(self)
        self.setupMyUi()
        self.setupSignals()

    def setupSignals(self):
        # Other singals defined in Desinger.
        self.loginReturn.connect(self.checkLogin)
        self.chk_Remember.clicked.connect(self.uncheckAutoLogin)

    def accept(self, client):
        if self.chk_Remember.isChecked():
            self.passwd[str(self.username)] = str(self.password)
            self.last_login = str(self.username)
            # Because this is a model dislog,
            # closeEvent won't emit when we accept() the window, but will
            # emit when we reject() the window.
            self.saveConfig()
        wecase_main = WeCaseWindow()
        wecase_main.init_account(client)
        wecase_main.show()
        # Maybe users will logout, so reset the status
        self.pushButton_log.setText(self.tr("GO!"))
        self.pushButton_log.setEnabled(True)
        self.done(True)

    def reject(self):
        QtGui.QMessageBox.critical(None, self.tr("Authorize Failed!"),
                                   self.tr("Check your account, "
                                           "password and Internet Connection!")
                                  )
        self.pushButton_log.setText(self.tr("GO!"))
        self.pushButton_log.setEnabled(True)

    def checkLogin(self, client):
        if client:
            self.accept(client)
        else:
            self.reject()

    def setupMyUi(self):
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
        self.config = ConfigParser()
        self.config.read(const.config_path)

        if not self.config.has_section('login'):
            self.config['login'] = {}

        self.login_config = self.config['login']
        self.passwd = eval(self.login_config.get('passwd', "{}"))
        self.last_login = str(self.login_config.get('last_login', ""))
        self.auto_login = self.login_config.getboolean('auto_login', 0)

    def saveConfig(self):
        self.login_config['passwd'] = str(self.passwd)
        self.login_config['last_login'] = self.last_login
        self.login_config['auto_login'] = str(self.chk_AutoLogin.isChecked())

        with open(const.config_path, "w+") as config_file:
            self.config.write(config_file)

    def login(self):
        self.pushButton_log.setText(self.tr("Login, waiting..."))
        self.pushButton_log.setEnabled(False)
        self.ui_authorize()

    def ui_authorize(self):
        self.username = self.cmb_Users.currentText()
        self.password = self.txt_Password.text()
        threading.Thread(group=None, target=self.authorize,
                         args=(self.username, self.password)).start()

    def authorize(self, username, password):
        # TODO: This method is very messy, maybe do some cleanup?

        client = APIClient(app_key=const.APP_KEY, app_secret=const.APP_SECRET,
                           redirect_uri=const.CALLBACK_URL)

        # Step 1: Get the authorize url from Sina
        authorize_url = client.get_authorize_url()

        # Step 2: Send the authorize info to Sina and get the authorize_code
        # TODO: Rewrite them with urllib/urllib2
        oauth2 = const.OAUTH2_PARAMETER
        oauth2['userId'] = username
        oauth2['passwd'] = password
        postdata = urllib.parse.urlencode(oauth2)

        conn = http.client.HTTPSConnection('api.weibo.com')
        try:
            conn.request('POST', '/oauth2/authorize', postdata,
                         {'Referer': authorize_url,
                          'Content-Type': 'application/x-www-form-urlencoded'})
        except OSError:
            self.loginReturn.emit(None)
            return

        res = conn.getresponse()

        location = res.getheader('location')

        if not location:
            return self.loginReturn.emit(None)

        authorize_code = location.split('=')[1]
        conn.close()

        # Step 3: Put the authorize information into SDK
        r = client.request_access_token(authorize_code)
        access_token = r.access_token
        expires_in = r.expires_in

        client.set_access_token(access_token, expires_in)
        self.loginReturn.emit(client)

    def setPassword(self, username):
        if username:
            self.txt_Password.setText(self.passwd[str(username)])

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
