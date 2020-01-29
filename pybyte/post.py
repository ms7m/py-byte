

import requests
import json
from loguru import logger
from pybyte.endpoints import Endpoints
import arrow
import pathlib
from pybyte.session import ByteSession
from pybyte.feed import ByteFeed

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


class BytePost(object):
    def __init__(self, post_id, session=False):
        self._post_id = post_id
        self._session = session

        if session == False:
            raise Exception("no session provided.")
        else:
            if isinstance(session, ByteSession) == True:
                self._session = session.session()
            else:
                if isinstance(session, requests.Session) == True:
                    self._session = session
                else:
                    raise Exception("Unknown session provided.")
        self._load()

    def _load(self):
        try:
            req = self._session.get(
                Endpoints.POST_INFO + self._post_id
            )

            if req.status_code == 200:
                req_parse = req.json()
                if check_for_success(req_parse) == True:
                    self._post_info = req_parse['data']
                else:
                    logger.debug(req.text)
                    raise Exception('Unable to get byte post: couldnt parse json')
            else:
                raise Exception(f'Byte API Failed: status code not 200. It is {req.status_code}')
        except Exception as error:
            logger.error(f"outer block fail: {req.status_code}")


    @property
    def author(self):
        from pybyte.user import ByteUser
        return ByteUser(self._post_info['authorID'], self._session)

    @property
    def caption(self):
        return self._post_info['caption']

    @property
    def date(self):
        return arrow.get(self._post_info['date']).datetime

    @property
    def comment_count(self):
        return self._post_info['commentCount']

    @property
    def like_count(self):
        return self._post_info['likeCount']
    
    @property
    def rebyte_by_me(self):
        return self._post_info['rebytedByMe']

    @property
    def mentions(self):
        from pybyte.user import ByteUser
        if self._post_info.get('mentions', False) != False:
            return [ByteUser(user['accountID'], self._session) for user in self._post_info['mentions']]
        else:
            return []

    def likes(self):
        from pybyte.user import ByteUser
        try:
            req_send = self._session.get(
                Endpoints.LIKE(self._post_id), data=convert_dict({'postID': self._post_id})
            )
            if req_send.status_code == 200:
                return [ByteUser(user['id'], self._session) for user in req_send.json()['data']['accounts']]
            else:
                logger.error(f"status code not 200: {req_send.status_code}")
                logger.debug(req_send.texts)
                return False
        except Exception as error:
            logger.error(f'rebyte error: {error}')
            return False        



    def rebyte(self):
        
        try:
            req_send = self._session.post(
                Endpoints.REBYTE, data=convert_dict({'postID': self._post_id})
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

    def un_rebyte(self):
        try:
            req_send = self._session.delete(
                Endpoints.UNREBYTE(self._post_id)
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
            
    def unlike(self):
        try:
            req_send = self._session.delete(
                Endpoints.LIKE(self._post_id), data=convert_dict({'postID': self._post_id})
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


    def like(self):
        try:
            req_send = self._session.put(
                Endpoints.LIKE(self._post_id), data=convert_dict({'postID': self._post_id})
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

    
    def comment(self, string):
        try:
            req_send = self._session.post(
                Endpoints.COMMENT(self._post_id), data=convert_dict({'postID': self._post_id, 'body': string})
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

