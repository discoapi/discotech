import sys
import urllib
import json
import time

import discotech.utils
from discotech.errors import discotechError

__package__ = 'APIProviders'

class Provider(object):
    """
    A general class to describe an API provider
    """

    def __init__(self, url, name = None, auth_type_search='none'):
        """
        @type  url: str
        @param url: provider api url

        Optional Parametars
        
        @type  name: str
        @param name: Provider's name
        @type  auth_type_search: str
        @param auth_type_search: the provider authentication method possible value are 'none','api_key','oauth_1','oauth_2'
        
        """
        # required arguments
        self.url = url

        #default arguments
        self.auth_type_search = auth_type_search

        #optional arguments
        if name:
            self.name = name
        
        
    #for initing a provider for a JSON record from Configuration File
    @classmethod
    def initFromDict(cls, data):
        """
        Factory Method
        create a new provider from a configuration dict

        example:

        >>> provider = discotech.Provider.initFromDict({'name':'YouTube','url':'...'})
        >>> print(vars(provider))
        {'auth_type_search': 'none', 'name': 'YouTube', 'url': '...'}
        
        @type  data: dict
        @param data: a configuraion dict

        @return: new Prorivder
        """
        provider = Provider(data['url'])
        Provider._updateProviderFromDict(provider,data)
        return provider


    def updateFromDict(self, data):
        """
        update the provider data from config data

        exmaple:
        
        >>> provider = discotech.Provider(url='')
        >>> config = { 'name':'YouTube', 'auth_type_search': 'api_key', 'auth_value':{'api_key':'...'}}
        >>> provider.updateFromDict(config)
        >>> print(vars(provider))
        {'auth_type_search': 'api_key', 'auth_value': {'api_key': '...'}, 'name': 'YouTube', 'url': ''}
        
        @type  data: dict
        @param data: provider configuration
        """
        Provider._updateProviderFromDict(self,data)
        
    @classmethod
    def _updateProviderFromDict(cls,provider,data):

        if 'name' in data:
            provider.name = data['name']
        if 'url' in data:
            provider.url = data['url']
        if 'auth_type_search' in data:
            provider.auth_type_search = data['auth_type_search']
        
        if 'rl_hits_remaining' in data and data['rl_hits_remaining']!=None:
            provider.rl_hits_remaining = data['rl_hits_remaining'].strip()

        if 'rl_next_window' in data and data['rl_next_window']!=None:
            provider.rl_next_window = data['rl_next_window'].strip()

        if 'rl_hits_per_window' in data and data['rl_hits_per_window']!=None:
            provider.rl_hits_per_window = data['rl_hits_per_window'].strip()

        if 'auth_value' in data and data['auth_value']!='':
            credentials = data['auth_value']
            if provider.auth_type_search=='oauth_1':
                clientKey = credentials['oauth_client_key']
                clientSecret = credentials['oauth_client_secret']
                tokenIdentifier = credentials['oauth_token_identifier']
                tokenSecret = credentials['oauth_token_secret']
                provider.setOAuth(clientKey,clientSecret,tokenIdentifier,tokenSecret)
                
            if provider.auth_type_search=='oauth_2':
                accessToken = credentials['oauth2_access_token']
                tokenExpireTimestamp = credentials['oauth2_token_expire_timestamp'] if 'oauth2_token_expire_timestamp' in credentials else None
                clientId = credentials['oauth2_client_id'] if 'oauth2_client_id' in credentials else None
                clientSecret = credentials['oauth2_client_secret'] if 'oauth2_client_secret' in credentials else None
                refreshToken = credentials['oauth2_refresh_token'] if 'oauth2_refresh_token' in credentials else None
                refreshTokenUrl = credentials['oauth2_refresh_token_url'] if 'oauth2_refresh_token_url' in credentials else None
                provider.setOAuth2(accessToken,tokenExpireTimestamp,clientId,clientSecret,refreshToken,refreshTokenUrl)
                
            if provider.auth_type_search =='api_key':
                APIKey = credentials['api_key']
                provider.setAPIKey(APIKey)
                
                
    def setOAuth(self, clientKey, clientSecret, tokenIdentifier, tokenSecret):
        """
        set the OAuth Credentials

        @type  clientKey: str
        @param clientKey: OAuth Client Key
        @type  clientSecret: str
        @param clientSecret: OAuth Client Secret
        @type  tokenIdentifier: str
        @param tokenIdentifier: OAuth Token Identifier
        @type  tokenSecret: str
        @param tokenSecret: OAuth Token Identifier
        """
        self.auth_type_search = 'oauth_1'

        self.auth_value = {
            'oauth_client_key' : clientKey,
            'oauth_client_secret' : clientSecret,
            'oauth_token_identifier' : tokenIdentifier,
            'oauth_token_secret' : tokenSecret
        }

    def setAPIKey(self,APIKey):
        """
        set the api key credentials

        @type  APIKey: str
        @param APIKey: the api key
        """
        self.auth_type_search = 'api_key'

        self.auth_value = {
            'api_key' : APIKey
        }

    def isSearchable(self):
        """
        @return: checks if the provider can be searched

        @rtype: Bool
        """
        if self.auth_type_search == 'none':
            return True

        if self.auth_type_search == 'api_key':
            try:
                self.auth_value['api_key']
                return True
            except AttributeError:
                return False

        if self.auth_type_search == 'oauth_1':
            try:
                self.auth_value['oauth_client_key']
                return True
            except AttributeError:
                return False

	if self.auth_type_search == 'oauth_2':
	    return 'oauth2_access_token' in self.auth_value
                  
    def setOAuth2(self, accessToken , tokenExpireTimestamp = None, clientId = None, clientSecret = None, refreshToken = None, refreshTokenUrl = None):
        """
        set the OAuth2 credentails to access the provider

        @type  accessToken: str
        @param accessToken: oauth2 access token

        Optional Parametars:
        @type  tokenExpireTimestamp: int
        @param tokenExpireTimestamp: when will the oauth2 token will expire

        Needed only for refreshing tokens
        @type  clientId: str
        @param clientId: your application client id
        @type  clientSecret: str
        @param clientSecret: your application client secret
        @type  refreshToken: str
        @param refreshToken: the access token refresh token
        @type  refreshTokenUrl: str
        @param  refreshTokenUrl: the url used to refresh the access token
        """
        self.auth_type_search = 'oauth_2'

        # required value
        self.auth_value = {
            'oauth2_access_token': accessToken,
        }

        #optional arguments
        if tokenExpireTimestamp:
            self.auth_value['oauth2_token_expire_timestamp'] = tokenExpireTimestamp

        # arguments for refreshing tokens
        if clientId:
            self.auth_value['oauth2_client_id'] = clientId

        if clientSecret:
            self.auth_value['oauth2_client_secret'] = clientSecret

        if refreshToken:
            self.auth_value['oauth2_refresh_token'] = refreshToken

        if refreshTokenUrl:
            self.auth_value['oauth2_refresh_token_url'] = refreshTokenUrl

    def isOAuth2Refreshable(self):
        """
        @return: can the provider refresh his oauth2 token

        this applies moslty for google where oauth2 token have to be refreshed every 2 hours

        @rtype: Bool
        """

        requiredFields = ['oauth2_refresh_token_url','oauth2_refresh_token','oauth2_client_id','oauth2_client_secret']

        for requiredField in requiredFields:
            if not requiredField in self.auth_value:
                return False

        return True

                    
    def toDict(self):
        """
        creates a dict from which you can later create a copy of the class

        usefull to serialize class instances
        """
        #object == json record
        retDict = dict(self.__dict__)
        #rename url to url
        retDict['url'] = retDict.pop('url')
        return retDict

        
    
    def refreshOAuth2Token(self):
        """
        tries to refresh the provider oauth2 token

        this applies moslty for google where oauth2 token have to be refreshed every 2 hours
        """
        if self.auth_type_search != 'oauth_2':
            raise discotechError('Not a OAuth2 provider')

        #prepare refresh token fields

        postFields = {
            'refresh_token' : self.auth_value['oauth2_refresh_token'],
            'client_id' : self.auth_value['oauth2_client_id'],
            'client_secret' : self.auth_value['oauth2_client_secret'],
            'grant_type' : 'refresh_token'
        }

        if (3, 0) <= sys.version_info:
            encodedpostField = urllib.parse.urlencode(postFields)
        else:
            encodedpostField = urllib.urlencode(postFields)

        newToken = discotech.utils.getUrlContents(self.auth_value['oauth2_refresh_token_url'],encodedpostField,
                                        {},{'Content-Type': 'application/x-www-form-urlencoded'})
        
        #parse the response, this works only with google
        newToken = json.loads(newToken['response_text'])

        self.auth_value['oauth2_access_token'] = newToken['access_token']
        self.auth_value['oauth2_token_expire_timestamp'] = int(time.time()) + newToken['expires_in']



    def search(self,keyword):
        """
        search the provider

        @type  keyword: str
        @param keyword: the keyword to search for

        @rtype:  str
        @return: the response from the provider
        """
        return discotech.utils.provider_query(self,keyword)


    
    def searchUrl(self,url):
        """
        search the provider but with a different url
        this is usefull when you parsed the provider reponse and have a url for the next
        you don't to create a new provider instance

        @type  url: str
        @param url: the url to search

        @rtype:  str
        @return: the response from the provider
        """
        originalProvider = self.url
        # switch temporarly to next page url
        self.url = url
        retVal = self.search('')
        # bring back url
        self.url = originalProvider
        return retVal
