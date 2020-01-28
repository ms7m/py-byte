


import requests
import json
from loguru import logger
from pybyte.endpoints import Endpoints
import arrow
import pathlib
import copy
from pybyte.session import ByteSession

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
    def __reload(self):
        try:
            get_new = self._internalSession.get(
                Endpoints.ACCOUNT
            ).json()
            self.__init__(get_new, self._internalSession)
        except Exception as error:
            raise Exception(f"Unable to reload byte account data: {error}")

    def __init__(self, user_information, session=False):
        if user_information.get('data', False) == False:
            self.__prelimData = user_information
        else:
            self.__prelimData = user_information['data']

        if session == False:
            raise Exception("no session provided.")
        else:
            if isinstance(session, ByteSession) == True:
                self._internalSession = session.session()
            else:
                if isinstance(session, requests.Session) == True:
                    self._internalSession = session
                else:
                    raise Exception("Unknown session provided.")
                #self._internalSession = session
            
        json.dump(self.__prelimData, open('user.json', 'w+'))
        self._userAccount = None


    @property
    def display_name(self):
        return self.__prelimData['displayName']
    
    @display_name.setter
    def display_name(self, value):
        try:
            copiedData = copy.deepcopy(self.__prelimData)
            copiedData['displayName'] = value
            attempt_request = self._internalSession.put(
                Endpoints.ACCOUNT, convert_dict(copiedData)
            )
            if attempt_request.status_code == 200:
                if check_for_success(attempt_request.json()) == True:
                    # refresh the prelim changes
                    self.__reload()
                else:
                    raise Exception("Unable to set bio: Byte returned a failed attempt.")
            else:
                raise Exception(f"Unable to set bio: Byte returned a non 200. {attempt_request.status_code}")

        except Exception as error:
            logger.error(f"error on setting bio: {error}")

    @property
    def bio(self):
        return self.__prelimData['bio']
    
    @bio.setter
    def bio(self, value):
        try:
            copiedData = copy.deepcopy(self.__prelimData)
            copiedData['bio'] = value
            attempt_request = self._internalSession.put(
                Endpoints.ACCOUNT, convert_dict(copiedData)
            )
            if attempt_request.status_code == 200:
                if check_for_success(attempt_request.json()) == True:
                    # refresh the prelim changes
                    self.__reload()
                else:
                    raise Exception("Unable to set bio: Byte returned a failed attempt.")
            else:
                raise Exception(f"Unable to set bio: Byte returned a non 200. {attempt_request.status_code}")

        except Exception as error:
            logger.error(f"error on setting bio: {error}")

    @property
    def username(self):
        return self.__prelimData['username']

    @username.setter
    def username(self, value):
        try:
            copiedData = copy.deepcopy(self.__prelimData)
            copiedData['username'] = value
            attempt_request = self._internalSession.put(
                Endpoints.ACCOUNT, convert_dict(copiedData)
            )
            if attempt_request.status_code == 200:
                if check_for_success(attempt_request.json()) == True:
                    # refresh the prelim changes
                    self.__reload()
                else:
                    raise Exception("Unable to set username: Byte returned a failed attempt.")
            else:
                raise Exception(f"Unable to set username: Byte returned a non 200. {attempt_request.status_code}")

        except Exception as error:
            logger.error(f"error on setting username: {error}")
            
    def user(self):
        return ByteUser(self.__prelimData['id'], self._internalSession)


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