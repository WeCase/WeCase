import sys
sys.path.append("..")
from weibos.client import UBClient
import const


SUCCESS = 1
PASSWORD_ERROR = -1
NETWORK_ERROR = -2


def UBAuthorize(username, password):
    client = UBClient(app_key=const.APP_KEY,
                      app_secret=const.APP_SECRET,
                      redirect_uri=const.CALLBACK_URL)

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
