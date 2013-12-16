import json

from .errors import discotechError
from .APIProviders.provider import Provider
from .APIProviders.providerSearcher import ProviderSearcher
from .discoAPI.discoAPIParser import DiscoAPIParser
from .discoAPI.keywordManager import KeywordManager
from .discoAPI.discoAPISearcher import DiscoAPISearcher

__package__ = 'discotech'


#internal instances
providerSearcher = ProviderSearcher()
discoAPIParser = DiscoAPIParser()
keywordManager = KeywordManager()
discoAPISearcher = DiscoAPISearcher()

#discotech functionality
def loadConfig(config):
        #if it's dict
        if type(config) is dict:
                #try to load providers
                if 'providers' in config:
                        providerSearcher.loadConfig(config['providers'])
                #try to load parser
                if 'parser' in config:
                        discoAPIParser.loadConfig(config['parser'])
                #try to load searcher

                #try to load keyword manager
                if 'keywords' in config:
                        keywordManager.loadConfig(config['keywords'])

                return (providerSearcher,discoAPIParser,keywordManager)
                
        #if it's string
        isString = None
        # python 2 vs 3
        try:
            isString = isinstance(config, basestring)
        except NameError:
            isString = isinstance(config, str)
        
        if isString:
                #could be an address
                if config.startswith('http://') or config.startswith('https://'):
                        configFile = getUrlContents(config)
                        confDict = json.loads(configFile['response_text'])
                        #recursivly call yourself
                        return loadConfig(confDict)
                #could be file name
                confFile = open(config,'r')
                confDict = json.loads(confFile.read())

                #recursivly call yourself
                return loadConfig(confDict)
