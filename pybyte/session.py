
import requests

class ByteSession(object):
    def __init__(self, token, providedSession=False):
        self._userToken = token
        if providedSession == False:
            self._session = requests.session()
        else:
            self._session = providedSession

        self._session.headers = {
            "Authorization":  token,
            "User-Agent": "byte/0.2 (co.byte.video; build:145; iOS 13.3.0) Alamofire/4.9.1"
        }


    def session(self):
        return self._session