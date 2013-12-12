__package__ = 'discotech'

class KeywordManager(object):
    """
    Simple object to store and queue keyword to search in social media providers
    """
    
    def __init__(self,keywords):
        """
        @type  keywords: list
        @param keywords: the keyword you want search for
        """
        self.keywords = keywords
        self._keywordCount = len(keywords)
        self._headLocation = 0

    def dequque(self):
        """
        dequque a keyword from the queue, the keyword is then moved to the end of the queue

        @return: the next keyword in queue
        """
        retValue = self.keywords[self._headLocation]
        # move head next
        self._headLocation = (self._headLocation + 1) % self._keywordCount

        return retValue


    @classmethod
    def loadConfig(cls,config):
        #if it's list
        if type(config) is list:
                return KeywordManager(config)
        #if it's string
        if type(config) is str:
                #could be an address
                if config.startswith('http://') or config.startswith('https://'):
                        configFile = getUrlContents(config)
                        confList = json.loads(configFile['response_text'])
                        #recursivly call yourself
                        return KeywordManager.loadConfig(confList)
                #could be file name
                confFile = open(config,'r')
                confLisr = json.loads(confFile.read())

                #recursivly call yourself
                return KeywordManager.loadConfig(confList)
