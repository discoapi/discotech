__package__ = 'discotech.discoAPI'

from discotech import discotechError

class KeywordManager(object):
    """
    Simple object to store and queue keyword to search in social media providers
    """
    
    def __init__(self,keywords = [],convertToSearchPhrases = False):
	"""
	@type  keywords: list
	@param keywords: the keyword you want search for
	@type  convertToSearchPhrases: bool
	@param convertToSearchPhrases: whether keyword should be conveted to matching search phrases for example 'spider man' => ['spider','man','spiderman','spider_man']
	"""
	if keywords: 
	    self.keywords =  self._keyworsToSearchPhrases(keywords) if convertToSearchPhrases else list(keywords)
	    self._keywordCount = len(self.keywords)
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
	self.keywords = list(keywords)
	self._keywordCount = len(self.keywords)
	self._headLocation = 0

    def _updateFromDict(self,config):
	if 'keywords' in config:
	    convertToSearchPhrases = False
	    if 'search_phrase' in config and config['search_phrase'] is True:
		convertToSearchPhrases = True
	    self.keywords = self._keyworsToSearchPhrases(config['keywords']) if convertToSearchPhrases else list(config['keywords'])
	    self._keywordCount = len(self.keywords)
	    self._headLocation = 0
	else:
	    raise discotechError("no keywords were given")
	    
    def _keyworToSearchPhrases(self,keyword):
	words = keyword.split(' ')

	#edge case
	if len(words) == 1:
	    return words

	cleanWords = []
	#cleanup stage
	for word in words:
	    word = word.strip()
	    if word != '':
		cleanWords.append(word)

	#combinator stage
	combinators = ['','_']
	combinedWords = []
	for combinator in combinators:
	    combinedWords.append(combinator.join(cleanWords))

	return cleanWords + combinedWords
	
	    
    def _keyworsToSearchPhrases(self,keywords):
	retList = []
	for keyword in keywords:
	    retList += self._keyworToSearchPhrases(keyword)
	return retList
	    
    def loadConfig(self,config):
	"""
	load keywords from a configuation

	@type  config: list | str
	@param config: a list of keywords or a path or address of JSON configuration file
	"""
	#if it's list
	if type(config) is list:
	    self._updateFromList(config)

	#if it's a dict
	if type(config) is dict:
	    self._updateFromDict(config)
	    
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
