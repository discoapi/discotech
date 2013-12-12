__package__ = 'discotech.discoAPI'

from discotech import discotechError

class KeywordManager(object):
    """
    Simple object to store and queue keyword to search in social media providers
    """
    
    def __init__(self,keywords = []):
        """
        @type  keywords: list
        @param keywords: the keyword you want search for
        """
	if keywords: 
	    self.keywords = keywords
	    self._keywordCount = len(keywords)
	    self._headLocation = 0
	else:
	    self.keywords = keywords

    def dequque(self):
        """
        dequque a keyword from the queue, the keyword is then moved to the end of the queue

        @return: the next keyword in queue
        """
	if not self.keywords:
	    raise discotechError("you don't any keywords")

	
        retValue = self.keywords[self._headLocation]
        # move head next
        self._headLocation = (self._headLocation + 1) % self._keywordCount

        return retValue

    def _updateFromList(self,keywords):
	self.keywords = keywords
	self._keywordCount = len(keywords)
	self._headLocation = 0
	    

    def loadConfig(self,config):
	"""
	load keywords from a configuation

	@type  config: list | str
	@param config: a list of keywords or a path or address of JSON configuration file
	"""
        #if it's list
        if type(config) is list:
                self._updateFromList(config)
        #if it's string
        if type(config) is str:
                #could be an address
                if config.startswith('http://') or config.startswith('https://'):
                        configFile = getUrlContents(config)
                        confList = json.loads(configFile['response_text'])
                        #recursivly call yourself
                        return self.loadConfig(confList)
                #could be file name
                confFile = open(config,'r')
                confLisr = json.loads(confFile.read())

                #recursivly call yourself
                return self.loadConfig(confList)
