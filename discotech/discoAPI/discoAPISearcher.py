import json
import urllib
import requests
import discotech

__package__ = 'discotech.discoAPI'

class DiscoAPISearcher(object):
    """
    a class to search results from cached data in discoAPI
    """

    def __init__(self,discoAPIKey = ""):
        self.__discoAPIKey = discoAPIKey


    def setDiscoAPIKey(self,api_key):
        """
        set you discoAPIKey

        @param api_key: your discoAPI key
        @type  api_key: str
        """
        self.__discoAPIKey = api_key

        
    def search(self,**kwargs):
        """
        search discoAPI using API parametars

	@type  kwargs: packed dict
	@param kwargs: any discoAPI acceptable argument for more info see https://discoapi.com/docs/search/search.html
        """

        if self.__discoAPIKey == "":
            raise discotech.discotechError('you must supply an api key')
        
        # prepare your parametars
        data = {'api_key' : self.__discoAPIKey}
        # add arguments
        data.update(**kwargs)
        # prepare url
        url = 'https://discoapi.com/api/query/'+urllib.quote(json.dumps(data))
        # get response
        jsonResponse = requests.get(url)
        # parse response
        response = json.loads(jsonResponse.text)

        return response
