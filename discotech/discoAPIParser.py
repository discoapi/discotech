import json
import discotech
from .parseResults import ParseResults

__package__ = 'discotech'

class DiscoAPIParser(object):

    def __init__(self,discoAPIKey,toCacheResults = True,returnResults = False):
        self._discoAPIKey = discoAPIKey
        self._toCacheResults = toCacheResults
        self._returnResults = returnResults

    def parse(self,results,providerName,keyword):
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
        
            
    @classmethod
    def loadConfig(cls,config):
        #if it's dict (single item config)
        if type(config) is dict:
            #fix this
            return DiscoAPIParser(config['api_key'],config['cache'],config['return_results'])
        #if it's string
        if type(config) is str:
            #could be an address
            if config.startswith('http://') or config.startswith('https://'):
                configFile = getUrlContents(config)
                confDict = json.loads(configFile['response_text'])
                #recursivly call yourself
                return DiscoAPIParser.loadConfig(confDict)
            #could be file name
            confFile = open(config,'r')
            confDict = json.loads(confFile.read())
            
            #recursivly call yourself
            return DiscoAPIParser.loadConfig(confDict)


    
        
