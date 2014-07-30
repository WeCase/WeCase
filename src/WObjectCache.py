# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented a very simple object cache by
#           using dict hashes.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


from WeHack import Singleton


class WObjectCache(metaclass=Singleton):

    def __init__(self):
        self.__objects = {}

    def __calculate_key(self, object, key):
        return str(id(object)) + str(key)

    def open(self, object, key, *args):
        # TODO: Using LRU Cache to free memory.
        hash_key = self.__calculate_key(object, key)
        if hash_key in self.__objects.keys():
            return self.__objects[hash_key]
        obj = object(key, *args)
        self.__objects[hash_key] = obj
        return obj
