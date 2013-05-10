#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file defined constants and runtime constants.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import sys
import os


APP_KEY = "1011524190"
APP_SECRET = "1898b3f668368b9f4a6f7ac8ed4a918f"
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
OAUTH2_PARAMETER = {'client_id': APP_KEY,
                    'response_type': 'code',
                    'redirect_uri': CALLBACK_URL,
                    'action': 'submit',
                    'userId': '',  # username
                    'passwd': '',  # password
                    'isLoginSina': 0,
                    'from': '',
                    'regCallback': '',
                    'state': '',
                    'ticket': '',
                    'withOfficalFlag': 0}
config_path = os.environ['HOME'] + '/.config/wecase/config_db'
cache_path = os.environ['HOME'] + '/.cache/wecase/'
myself_name = sys.argv[0].split('/')[-1]
myself_path = os.path.abspath(sys.argv[0]).replace(myself_name, "")
