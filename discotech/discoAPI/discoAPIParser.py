import json
import discotech
from .parseResults import ParseResults

__package__ = 'discotech.discoAPI'

class DiscoAPIParser(object):
    """
    a class to parse results from social media providers througth the discoAPI parse API
    """
    
    def __init__(self,discoAPIKey = "",toCacheResults = True,returnResults = False):
	"""
	@type  discoAPIKey: str
	@param discoAPIKey: your discoAPI api key
	@type  toCacheResults: bool
	@param toCacheResults: whether to chache results to discoAPI for later use with search API
	@type  returnResults: bool
	@param returnResults: whether to return the parsed results after parsing
	"""
	self._discoAPIKey = discoAPIKey
	self._toCacheResults = toCacheResults
	self._returnResults = returnResults

    def parse(self,results,providerName,keyword):
	"""
	parse results from social media with discoAPI
	
	@type  results: str
	@param results: the results you got from the social media provider
	@type  providerName: str
	@param providerName: the name of the provider you are trying to parse (see discoAPI parse api docs to see what options are avalible)
	@type  keyword: str
	@param keyword: the keyword you searched for, it's needed so you can later find results by this keyword
    
	@rtype: ParseResults
	@return: the discoAPI response
	"""

	if self._discoAPIKey == "":
	    raise discotech.discotechError('you must supply an api key')
	
	postData = {
	    'api_key': self._discoAPIKey,
	    'provider': providerName,
	    'data': results,
	    'keyword': keyword,
	    'cache': self._toCacheResults,
	    'return_results': self._returnResults
	}

	postData_json = json.dumps(postData)
    
	# response from DiscoAPI
	url_contents = discotech.getUrlContents('https://discoapi.com/api/parse',postData_json)

	return ParseResults(url_contents['response_text'])
	

    def _updateFromDict(config):
	self._discoAPIKey = config['api_key']
	self._toCacheResults = config['cache']
	self._returnResults = config['return_results']

    
    def loadConfig(self,config):
	"""
	load parser configuation

	@type  config: dict | str
	@param config: parser configuration dict or a path or address of JSON configuration file
	"""
	#if it's dict (single item config)
	if type(config) is dict:
	    return self._updateFromDict(config)
	#if it's string
	if type(config) is str:
	    #could be an address
	    if config.startswith('http://') or config.startswith('https://'):
		configFile = getUrlContents(config)
		confDict = json.loads(configFile['response_text'])
		#recursivly call yourself
		return self.loadConfig(confDict)
	    #could be file name
	    confFile = open(config,'r')
	    confDict = json.loads(confFile.read())
	    
	    #recursivly call yourself
	    return self.loadConfig(confDict)


    
	
