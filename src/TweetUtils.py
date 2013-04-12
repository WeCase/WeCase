#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented a bug-for-bug compatible
#           strings' length counter with Sina's 
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import re
from math import ceil


def tweetLength(text):
    """ This function implemented a strings' length counter, the result of
    this function should be bug-for-bug compatible with Sina's."""

    def findall(regex, text):
        """ re.findall() sometimes output unexcepted results. This function
        is a special version of findall() """

        results = []

        re_obj = re.compile(regex)
        for match in re_obj.finditer(text):
            results.append(match.group())
        return results

    TWEET_MIN = 41
    TWEET_MAX = 140
    TWEET_URL_LEN = 20

    total = 0
    n = text
    if len(text) > 0:
        # please improve it if you can fully understand it
        r = findall(r"http://[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+([-A-Z0-9a-z_$.+!*()/\\\,:@&=?~#%]*)", text)

        for item in r:
            url = item
            byteLen = len(url) + len(re.findall(r"[^\x00-\x80]", url))

            if re.search(r"^(http://t.cn)", url):
                continue
            elif re.search(r"^(http:\/\/)+(weibo.com|weibo.cn)", url):
                total += (byteLen if byteLen <= TWEET_MIN else
                          (TWEET_URL_LEN if byteLen <= TWEET_MAX
                          else byteLen - TWEET_MAX + TWEET_URL_LEN))
            else:
                total += (TWEET_URL_LEN if byteLen <= TWEET_MAX else
                          (byteLen - TWEET_MAX + TWEET_URL_LEN))
            n = n.replace(url, "")
    return ceil((total + len(n) + len(re.findall(r"[^\x00-\x80]", n))) / 2)
