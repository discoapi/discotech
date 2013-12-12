import json

import discotech

from .errors import discotechError
from .provider import Provider

__package__ = 'discotech'

class ProviderSearcher(object):
    """
    class to help search and manage several providers
    """
    
    def __init__(self):
        #internal providers dict
        self._providers = {}

        #excluded config is stored here
        self._excludedConfig = {}
        

    def _excludeConfig(self,config):
        # remove name from config
        providerName = config.pop('name')
        excludedAttributes = []
        # save exluded values
        for key, value in config.items():
                excludedAttributes.append((key, value))
        #save exluded values for the provider
        if providerName in self._excludedConfig:
                self._excludedConfig[providerName] += excludedAttributes
        else:
                self._excludedConfig[providerName] = excludedAttributes
        

    def _addProviderFromConfig(self,config, saveConfig):
        provider = Provider.initFromDict(config)

        # only not excluded configs are saved
        if not saveConfig:
                self._excludeConfig(config)
        self.addProvider(provider)

    def _updateProviderFromConfig(self,config, saveConfig):
        self._providers[config['name']].updateFromDict(config)

        if not saveConfig:
                self._excludeConfig(config)
        
        
    def addProvider(self,provider):
        """
        add provider to providerSearcher

        provider name must be set

        @type  provider: Provider
        @param provider: provider to add
        """
        if not hasattr(provider,'name'):
                raise discotechError('Missing name for provider')
        
        self._providers[provider.name] = provider

    def addProviders(self,providers):
        """
        add several providers to ProviderSearcher

        @type  providers: list
        @param providers: providers to add
        """
        for provider in providers:
                addProvider(provider)

    def getProvider(self,providerName):
        """
        get a provider stored in the ProviderSearcher

        @type  providerName: str
        @param providerName: the name of the provider you want to get
        """
        return self._providers[providerName]
                
    def search(self,providerName,keyword):
        """
        search a stored provider

        @type  providerName: str
        @param providerName: the name of the provider you want to search
        @type  keyword: str
        @param keyword: the keyword to search

        @rtype: str
        @return: the response from the provider
        """
        if not providerName in self._providers:
                raise discotechError('Missing provider:'+providerName)
        return self._providers[providerName].search(keyword)

    def searchAll(self,keyword):
        """
        search all the provider stored in ProviderSearcher

        the provider must return True for isSearchable() method

        @type  keyword: str
        @param keyword: the keyword to search

        @rtype: dict
        @return: a dictionay where the keys are the provider name and the values are the provider responses
        """
        retDict = {}
        for providerName, provider in self._providers.items():
                retDict[providerName] = provider.search(keyword)
        return retDict


    def loadBaseConfig(self,config):
        """
        load a config object(dict or local file or url) but don't save it to local config
        this is similliar to loadConfig but doesn't affect the ProviderSearcher config

        this is usefull if you have a remote configuration for providers you don't to overwrite with saveConfig() method
        for example https://discoapi.com/api/providers.json

        @type  config: dict | str
        @param config: the config to load
        """
        self._loadConfig(config, False)

    def loadConfig(self,config):
        """
        load a config object(dict or local file or url)

        @type  config: dict | str
        @param config: the config to load
        """
        self._loadConfig(config, True)

    def _loadConfig(self,config, includeConfig):
        #if it's list
        if type(config) is list:
                for itemConfig in config:
                        self._loadConfig(itemConfig,includeConfig)
        #if it's dict (single item config)
        if type(config) is dict:
                #check if it's a new config or an update
                if config['name'] in self._providers:
                        #update
                        self._updateProviderFromConfig(config,includeConfig)
                else:
                        #new provider
                        self._addProviderFromConfig(config,includeConfig)
        #if it's string
        if isinstance(config,basestring):
                #could be an address
                if config.startswith('http://') or config.startswith('https://'):
                        configFile = discotech.getUrlContents(config)
                        confDict = json.loads(configFile['response_text'])
                        #recursivly call yourself
                        return self._loadConfig(confDict,includeConfig)
                #could be file name
                confFile = open(config,'r')
                confDict = json.loads(confFile.read())

                #recursivly call yourself
                return self._loadConfig(confDict,includeConfig)

    def getSearchableProviders(self):
        """
        @return: all the stored providers which return True for the isSearchable() method
        @rtype: bool
        """
        retList = []
        for providerName, provider in self._providers.items():
                if provider.isSearchable():
                        retList.append(provider)
        return retList
                
                
    def getConfig(self):
        """
        @rtype: dict
        @return: the current config of the ProviderSearcher and all stored providers

        this can be very usefull for serializing ProviderSearcher object
        """
        retList = []
        for providerName, provider in self._providers.items():
                retList.append(provider.toDict())
        #filter initial config
        #notice iterating over list while removing items from it
        listCount = len(retList)
        currentItem = 0
        while currentItem < listCount:
                provider = retList[currentItem]       	

                # should you filter this provider
                if provider['name'] in self._excludedConfig:
                        for key, value in self._excludedConfig[provider['name']]:
                                #print "{0} : {1}".format(key,value)
                                if provider[key] == value:
                                        del provider[key]
                        #if only name left
                        if len(provider.items()) == 1:
                                retList.remove(provider)
                                listCount = listCount-1
                        else:
                                currentItem = currentItem+1
                else:
                        #provider doesn't have excluded values
                        currentItem = currentItem+1
        #in single item no need for list
        if len(retList) == 1:
                return retList[0]
        else:
                return retList

    def saveConfig(self,filename):
        """
        save the current ProviderSearcher configuraion in JSON format

        @type  filename: str
        @param filename: the filename of the file to save to
        """
        configFile = open(filename,'w')
        jsonStr = json.dumps(self.getConfig(), sort_keys=False,indent=4, separators=(',', ': '))
        configFile.write(jsonStr)
        configFile.close()
