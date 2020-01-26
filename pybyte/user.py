


import requests
import json
from loguru import logger
from pybyte.endpoints import Endpoints
import arrow
import pathlib


def convert_dict(dict):
    return json.dumps(dict)

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

class ByteUser(object):
    def __init__(self, user_id, session):
        self._user_id = user_id
        self._session = session
        self._userAccount = self.info()['data']

    def info(self):
        try:
            req = self._session.get(
                Endpoints.OTHER_ACCOUNT + self._user_id
            )

            if req.status_code == 200:
                if check_for_success(req.json()) == True:
                    return req.json()
                else:
                    raise Exception("byte api error: status not good")
            else:
                raise Exception(f"byte api failure: is not 200. {req.status_code}")
        except Exception as error:
            logger.error(f'unable to load: {error}')

    @property
    def user_id(self):
        if self._userAccount == None:
            self.info()
        return self._userAccount['id']
        
    @property
    def username(self):
        if self._userAccount == None:
            self.info()
        
        return self._userAccount['username']
    @property
    def followers(self):
        if self._userAccount == None:
            self.info()
        return {
            "followers": self._userAccount['followerCount'],
            "following": self._userAccount['followingCount']
        }
    @property
    def registered(self):
        if self._userAccount == None:
            self.info()
        return arrow.get(self._userAccount['registrationDate']).datetime

    @property
    def following(self):
        return self._userAccount['isFollowing']

    @property
    def followed(self):
        return self._userAccount['isFollowed']

        
    def follow(self):
        try:
            req_send = self._session.put(
                Endpoints.FOLLOW(self._userAccount['id'])
            )
            if req_send.status_code == 200:
                return True
            else:
                logger.error(f"status code not 200: {req_send.status_code}")
                logger.debug(req_send.texts)
                return False
        except Exception as error:
            logger.error(f'rebyte error: {error}')
            return False
            
    def unfollow(self):
        try:
            req_send = self._session.put(
                Endpoints.FOLLOW(self._userAccount['id'])
            )
            if req_send.status_code == 200:
                return True
            else:
                logger.error(f"status code not 200: {req_send.status_code}")
                logger.debug(req_send.texts)
                return False
        except Exception as error:
            logger.error(f'rebyte error: {error}')
            return False
        

class ByteAccount(object):
    def __init__(self, user_information, session=False):
        if user_information.get('data', False) == False:
            self.__prelimData = user_information
        else:
            self.__prelimData = user_information['data']

        if session == False:
            raise Exception("no session provided.")
        else:
            self._internalSession = session

        json.dump(self.__prelimData, open('user.json', 'w+'))
        self._userAccount = None

    def user(self):
        return ByteUser(self.__prelimData['account']['id'], self._internalSession)

"""
    def info(self):
        try:
            req_info = self._internalSession.get(Endpoints.ACCOUNT)
            self._userAccount = req_info.json()['data']
            return self._userAccount
        except Exception as error:
            logger.error(f'unable to complete request: {error}')
            

    @property
    def user_id(self):
        if self._userAccount == None:
            self.info()
        return self._userAccount['id']
    
    @property
    def username(self):
        if self._userAccount == None:
            self.info()

        
        return self._userAccount['username']

    @property
    def followers(self):
        if self._userAccount == None:
            self.info()


        return {
            "followers": self._userAccount['followerCount'],
            "following": self._userAccount['followingCount']
        }

    @property
    def registered(self):
        if self._userAccount == None:
            self.info()
        return arrow.get(self._userAccount['registrationDate']).datetime
"""