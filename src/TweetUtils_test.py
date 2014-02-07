#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented the unit tests for TweetUtils.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


import unittest
from TweetUtils import tweetLength, get_mid


class TweetUtilsTest(unittest.TestCase):

    def test_tweetLength(self):
        self.assertEqual(tweetLength("【转基因"), 4)
        self.assertEqual(tweetLength("我司CEO！"), 5)
        self.assertEqual(tweetLength("8@&*%&b"), 4)
        self.assertEqual(tweetLength(" Test"), 3)
        self.assertEqual(tweetLength("   Test   "), 5)
        self.assertEqual(tweetLength("　　　Ｔｅｓｔｉｎｇ　　　　"), 14)

    def test_get_mid(self):
        self.assertEqual(get_mid("3591268992667779"), 'zCik3bc0H')
        self.assertEqual(get_mid("3591370117495972"), 'zCkX9vs2M')
        self.assertEqual(get_mid("3591291856713634"), 'zCiUVsawq')


if __name__ == "__main__":
    unittest.main()
