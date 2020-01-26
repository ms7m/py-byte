
import requests
from pybyte.endpoints import Endpoints
import json
import pathlib
from loguru import logger
from pybyte.session import ByteSession
from pybyte.user import ByteAccount, ByteUser
from pybyte.post import BytePost

from ffprobe import FFProbe
from ffmpy import FFmpeg




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



    def upload(self, file_path, caption=""):
        try:
            metadata = FFProbe(file_path)
            metadata_information = metadata.streams[0]
            if float(metadata_information.duration) > 6:
                raise Exception(f"that video is too long. {metadata_information.duration}")

        except Exception as error:
            raise Exception(f"FFProbe failed: {error}")

        try:
            logger.info("generating a thumbnail")
            ff = FFmpeg(
                inputs={file_path: None}, 
                outputs={"thumbnail.jpg": ['-ss', '00:00:4', '-vframes', '1']}
            )
            ff.run()
        except Exception as error:
            raise Exception(f'could not generate a thumbnail: {error}')

        # Get Upload Information
        upload_urls = {
            "video": None,
            "thumbnail": None
        }
            
        # Get thumbnail/video url

        try:

            video_data = {
                "contentType": "video/mp4"
            }

            req_url = self._session.post(Endpoints.UPLOAD, data=self.convert_dict(video_data))
            req_url_parsed = req_url.json()['data']
            
            try:
                upload_urls['video'] = {
                    'id': req_url_parsed['uploadID'],
                    'url': req_url_parsed['uploadURL'],
                    "contentType": video_data['contentType']
                }
                logger.info("gathered upload for video")
            except Exception as error:
                logger.error('cant get upload urls.')
                raise Exception(f"Unable to get upload urls: {error}")


            thumbnail_data = {
                "contentType": "image/jpeg"
            }
            
            req_url = self._session.post(Endpoints.UPLOAD, data=self.convert_dict(thumbnail_data))
            req_url_parsed = req_url.json()['data']
            try:
                upload_urls['thumbnail'] = {
                    'id': req_url_parsed['uploadID'],
                    'url': req_url_parsed['uploadURL'],
                    "contentType": thumbnail_data['contentType']
                }
                logger.info("gathered upload for thumbnail")
            except Exception as error:
                logger.error('cant get upload urls.')
                raise Exception(f"Unable to get upload urls: {error}")



        except Exception as error:
            logger.error(error)
            raise Exception('Upload failed.')


        # push thumbnail

        file_upload_thumbnail = {
            "file": open("thumbnail.jpg", 'rb')
        }
        try:
            headers = {
                "Content-Type": upload_urls['thumbnail']['contentType']
            }
            req_push = requests.put(upload_urls['thumbnail']['url'], headers=headers, data=file_upload_thumbnail['file'])
            if req_push.status_code == 200:
                logger.info("file seem to be uploaded.")
            else:
                logger.error(f"Unable to upload thumbnail: {req_push.status_code}")
                raise Exception(f'Upload error thumbnail: {req_push.status_code}')
        except Exception as error:
            logger.error(f"Thumbnail block upload failed. {error}")
            raise Exception("Unable to upload.")


        # push video
        file_upload_video = {
            "file": open(file_path, 'rb')
        }
        try:

            headers = {
                "Content-Type": upload_urls['video']['contentType']
            }

            req_push = requests.put(upload_urls['video']['url'], headers=headers, data=file_upload_video['file'])
            if req_push.status_code == 200:
                logger.info("file seem to be uploaded.")
            else:
                logger.error(f"Unable to upload video: {req_push.status_code}")
                raise Exception(f'Upload error video: {req_push.status_code}')
        except Exception as error:
            logger.error(f"Thumbnail block upload failed. {error}")
            raise Exception("Unable to upload.")


        # final push
        try:
            data_to_push = {
                "caption": caption,
                "thumbUploadID": upload_urls['thumbnail']['id'],
                "videoUploadID": upload_urls['video']['id']
            }

            data_condensed = self.convert_dict(data_to_push)

            req_push = self._session.post(Endpoints.POST, data=data_condensed)
            if req_push.status_code == 200:
                if self.check_for_success(req_push.json()) == True:
                    return BytePost(req_push.json()['data']['id'], self._session)
                else:
                    raise Exception(f"Byte API was successful, but api status failed.. {req_push.status_code}")
            else:
                raise Exception(f"Byte API returned a non 200. {req_push.status_code}")
        except Exception as error:
            logger.error(f"final upload block faied: {error}")
            raise Exception(f"Final upload failed: {error}")
