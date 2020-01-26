
import requests
from pybyte.endpoints import Endpoints
import json
import pathlib
from loguru import logger
from pybyte.session import ByteSession
from pybyte.user import ByteAccount, ByteUser
from pybyte.post import BytePost


class Byte(object):

    @staticmethod
    def convert_dict(dict):
        return json.dumps(dict)
    @staticmethod
    def check_for_success(response):
        try:
            get_success_code = response.get('success', False)

            if get_success_code == False:
                return False

            status_code = str(get_success_code)
            if status_code == "0":
                return False
            elif status_code == "1":
                return True
            else:
                logger.error(f'unknown status code: {status_code}')
                return False
        except Exception as error:
            logger.error(f'exception on checking for success: {error}')
            return False


    def __initalize_cached_json(self):
        try:
            attempted = open("user.json", 'r')
            attempt_json = json.load(attempted)
            self.__loginInformation = attempt_json
            return True
        except Exception as error:
            logger.error("unable to open cached login information.")
            return False

    
    def __login(self, sessionProvided=True):
        if sessionProvided == True:
            sessionProvided = self._internalSession
        else:
            sessionProvided = sessionProvided

        try:
            if self._providedToken == False:
                raise Exception("No google OAUTH token provided.")
            

            attempt_login = self._internalSession.post(
                Endpoints.GOOGLE_LOGIN, self.convert_dict({'token': self._providedToken})
            )
            if attempt_login.status_code == 200:
                request_parsed = attempt_login.json()
                if self.check_for_success(request_parsed) == True:
                    self.__loginInformation = request_parsed
                else:
                    logger.debug(request_parsed)
                    raise Exception("byte api failed.")
            else:
                logger.error(f"byte api failed: {attempt_login.status_code}")
                raise Exception("byte api failed")
        except Exception as error:
            logger.error(f"unable to log in beacuse of: {error}")
            raise Exception("byte failure")


    def __init__(self, google_token=True):
        self._internalSession = requests.session()
        self.__loginInformation = False
        self._providedToken = False

        if google_token == True:
            if pathlib.Path("user.json").exists() == True:
                __loadCache = self.__initalize_cached_json()
                if __loadCache == True:
                    logger.info('loaded from cache.')
                    self._session = ByteSession(self.__loginInformation['token']['token'], providedSession=self._internalSession).session()
                else:
                    self.__loginInformation = False
            else:
                raise Exception('unable to load cache, please reload with google ouath token')
                    
        else:
            self._providedToken = google_token
            self.__login()
            self._session = ByteSession(self.__loginInformation['data']['token']['token'], providedSession=self._internalSession).session()

    def me(self):
        return ByteAccount(self.__loginInformation, self._session)

    def get_post(self, post_id):
        return BytePost(post_id, self._session)

    def get_user(self, user_id):
        return ByteUser(user_id, self._session)