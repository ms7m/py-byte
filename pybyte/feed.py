from loguru import logger

class ByteFeed(object):
    def __init__(self, feed_url, feed_data, byteSession_provided, feedArrayReturnObject, feedArrayKey="posts"):
        self._entireFeed = feed_data
        self._providedData = self._entireFeed['data']
        self._internalSession = byteSession_provided
        self._feedArrayKey = feedArrayKey
        self._feedArrayReturnObject = feedArrayReturnObject
        self._feedURL = feed_url

    def __nextCursor(self, cursor):
        try:
            update_cursor = {
                "cursor": cursor
            }
            attempt_get = self._internalSession.get(
                self._feedURL, params=update_cursor
            )
            if attempt_get.status_code == 200:
                self.__init__(self._feedURL, attempt_get.json(), self._internalSession,
                              self._feedArrayReturnObject, feedArrayKey=self._feedArrayKey)
                return True
            else:
                raise Exception(f"Byte API failed to get next cursor. {attempt_get.status_code}")
        except Exception as error:
            logger.error(f"unable to complete block. {error}")
            raise Exception("Unable to complete next cursor.")

    @property
    def feed(self):
        currentEndOfList = self._providedData[self._feedArrayKey][-1]
        endOfFeed = False
        while endOfFeed == False:
            for item in self._providedData[self._feedArrayKey]:
                if item['id'] == currentEndOfList['id']:
                    try:
                        self.__nextCursor(self._entireFeed['data']['cursor'])
                    except Exception as error:
                        logger.error(f"error on going to next cursor: {error}")
                        endOfFeed = True
                else:
                    yield self._feedArrayReturnObject(item['id'], self._internalSession)

