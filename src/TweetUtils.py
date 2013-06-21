#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented a bug-for-bug compatible
#           strings' length counter with Sina's
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import re
from math import ceil
import const


def tweetLength(text):
    """
    This function implemented a strings' length counter, the result of
    this function should be bug-for-bug compatible with Sina's.

    >>> tweetLength("我司CEO与我司吉祥物...好大一坨！")
    16
    """

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


def get_mid(mid):
    """
    Convert a id string of a tweet to a mid string.
    You'll need a mid to generate an URL for a single tweet page.

    >>> get_mid("3591268992667779")
    'zCik3bc0H'
    """

    def baseN(num, base):
        """Convert the base of a decimal."""
        CHAR = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return ((num == 0) and "0") or \
               (baseN(num // base, base).lstrip("0") + CHAR[num % base])

    url = ""

    i = len(mid) - 7
    while i > -7:
        offset_1 = 0 if i < 0 else i
        offset_2 = i + 7
        num = mid[offset_1:offset_2]
        num = baseN(int(num), 62)

        if not len(num) == 1:
            # if it isn't the first char of the mid, and it's length less than
            # four chars, add zero at left for spacing
            num = num.rjust(4, "0")

        url = num + url

        i -= 7
    return url


def authorize(authorize_url, username, password):
    """Send the authorize info to Sina and get the authorize_code"""
    import urllib.request
    import urllib.parse
    import urllib.error
    import http.client
    import ssl
    import socket

    oauth2 = const.OAUTH2_PARAMETER
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


import unittest
class TweetUtilsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_tweetLength(self):
        self.assertEqual(tweetLength("【转基因食品在美国】1、FDA在管理上和普通食品同等对待；2、2012年，转基因玉米种植面积占所有玉米的88%，大豆是93%，棉花是94%；过去十年美国人吃了3万亿份转基因餐食。再说转基因是美国阴谋的，先查查EPA（美国环保局）、USDA(美国农业部）、FDA（美国食品和药品管理局）的网站吧。"), 132)
        self.assertEqual(tweetLength("我司CEO与我司吉祥物...好大一坨！"), 16)
        self.assertEqual(tweetLength("这个很长8@&$&*@Q&$&*%&*#Q&%*&587q385,,,35,46,46,0fdfjkhsvbsjkbfsdjkbfsjkhgvbsdbvdjska fjs松江府斯渡口附近卡洛斯看得见三个计算机法国//-*-啊 杰克森的风景三等分角疯狂的风景快速减肥加 解放思考了封建凯瑟琳风景诵读佛经三加夫克拉934892580395835lljj开放加阿斯附近克利斯朵夫加,.,.,53453p[][][]][][402358935kc"), 150)

    def test_get_mid(self):
        self.assertEqual(get_mid("3591268992667779"), 'zCik3bc0H')
        self.assertEqual(get_mid("3591370117495972"), 'zCkX9vs2M')
        self.assertEqual(get_mid("3591291856713634"), 'zCiUVsawq')


if __name__ == "__main__":
    unittest.main()
