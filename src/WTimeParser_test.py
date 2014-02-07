#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented the unit tests for WTimeParser.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


import unittest
from datetime import datetime
from WTimeParser import WTimeParser, tzoffset


class WTimeParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = WTimeParser()

    def test_parse(self):
        got_daytime = self.parser.parse("Sat Apr 06 00:49:30 +0800 2013")
        except_daytime = datetime(2013, 4, 6, 0, 49, 30, tzinfo=tzoffset(None, 28800))
        self.assertEqual(got_daytime, except_daytime)


if __name__ == "__main__":
    unittest.main()
