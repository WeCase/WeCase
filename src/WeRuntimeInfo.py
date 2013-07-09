from WeHack import singleton


@singleton
class WeRuntimeInfo(dict):
    def __init__(self, *args):
        dict.__init__(self, args)
