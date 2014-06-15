#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented a wrapper of sinaweibopy3
#           with helper functions.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


import sys
sys.path.append("..")
from weibos.client import UBClient
from WConfigParser import WConfigParser
import const
import path


SUCCESS = 1
PASSWORD_ERROR = -1
NETWORK_ERROR = -2


def _auth_info():
    login_config = WConfigParser(path.myself_path + "WMetaConfig",
                                 path.config_path, "login")
    key = login_config.app_key or const.APP_KEY
    secret = login_config.app_secret or const.APP_SECRET
    callback = login_config.redirect_uri or const.CALLBACK_URL
    return key, secret, callback


def UBAuthorize(username, password):
    key, secret, callback = _auth_info()
    client = UBClient(app_key=key, app_secret=secret, redirect_uri=callback)

    try:
        # Step 1: Get the authorize url from Sina
        authorize_url = client.get_authorize_url()

        # Step 2: Send the authorize info to Sina and get the authorize_code
        authorize_code = _authorize(authorize_url, username, password)
        if not authorize_code:
            return PASSWORD_ERROR

        # Step 3: Get the access token by authorize_code
        r = client.request_access_token(authorize_code)

        # Step 4: Setup the access token of SDK
        client.set_access_token(r.access_token, r.expires_in)
        const.client = client
        return SUCCESS
    except Exception:
        return NETWORK_ERROR


def _authorize(authorize_url, username, password):
    """Send the authorize info to Sina and get the authorize_code"""
    import urllib.request
    import urllib.parse
    import urllib.error
    import http.client
    import ssl
    import socket

    oauth2 = const.OAUTH2_PARAMETER
    key, secret, callback = _auth_info()

    oauth2["client_id"] = key
    oauth2["redirect_uri"] = callback

    oauth2['userId'] = username
    oauth2['passwd'] = password

    postdata = urllib.parse.urlencode(oauth2)

    conn = http.client.HTTPSConnection('api.weibo.com')
    sock = socket.create_connection((conn.host, conn.port), conn.timeout, conn.source_address)
    conn.sock = ssl.wrap_socket(sock, conn.key_file, conn.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)

    conn.request('POST', '/oauth2/authorize', postdata,
                 {'Referer': authorize_url,
                  'Content-Type': 'application/x-www-form-urlencoded'})

    res = conn.getresponse()
    location = res.getheader('location')

    if not location:
        return False

    authorize_code = location.split('=')[1]
    conn.close()
    return authorize_code
