from weibo import APIClient, APIError, _Callable, _Executable
from http.client import BadStatusLine
from urllib.error import URLError, ContentTooShortError


class UBClient(APIClient):

    def __init__(self, *args, **kwargs):
        super(UBClient, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):
        if "__" in attr:
            return super(UBClient, self).__getattr__(attr)
        return _UBCallable(self, attr)


class _UBCallable(_Callable):

    def __init__(self, *args, **kwargs):
        super(_UBCallable, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):
        if attr == "get":
            return _UBExecutable(self._client, "GET", self._name)
        elif attr == "post":
            return _UBExecutable(self._client, "POST", self._name)
        else:
            name = "%s/%s" % (self._name, attr)
            return _UBCallable(self._client, name)


class _UBExecutable(_Executable):

    # if you find out more, add the error code to the tuple
    UNREASONABLE_ERRORS = (21321)

    def __init__(self, *args, **kwargs):
        super(_UBExecutable, self).__init__(*args, **kwargs)

    def __call__(self, **kw):
        while 1:
            try:
                return super(_UBExecutable, self).__call__(**kw)
            except (BadStatusLine, ContentTooShortError, URLError, OSError, IOError):
                # these are common networking problems:
                # note: OSError/IOError = Bad CRC32 Checksum
                continue
            except APIError as e:
                # these are unreasonable API Errors:
                # note: May caused by bugs on Sina's server
                if e.error_code in self.UNREASONABLE_ERRORS:
                    continue
