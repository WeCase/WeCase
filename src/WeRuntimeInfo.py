from WeHack import Singleton


class WeRuntimeInfo(dict, metaclass=Singleton):
    def __init__(self, *args):
        dict.__init__(self, args)
