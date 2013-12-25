
import json

__package__ = 'discotech.discoAPI'

class ParseResults(object):
    """
    parse results that are returned from discoAPI
    """
    
    def __init__(self,results):
        """
        @type  results: str
        @param results: discoAPI response from the discoAPI parse API
        """
        
        try:
            resultsDict = json.loads(results)
            
        except ValueError:
            #print error
            print('bad json response: {0}'.format(results))
            # face results dict
            resultsDict = {'status': 500, 'next_page_url':'done'} 
            
        
        self._status = resultsDict['status']

        if self._status == 200:
            self._success = True
            self._nextPageUrl = resultsDict['next_page_url']
            if 'results' in resultsDict:
                self._results = resultsDict
        else:
            self._success = False
            
    def hasMorePages(self):
        """
        rtype: bool
        @return: was the next page to search was returned in the parse results 
        """
        if self._success != True:
            return False
        if self._nextPageUrl != 'done':
            return True
        else:
            return False

    def nextPageUrl(self):
        """
        @rtype: str
        @return: the next page to search for results 
        """
        return self._nextPageUrl

    def hasResults(self):
        """
        @rtype: bool
        @return: was the parse response included discoAPI results 
        """
        return hasattr(self,'_results')

    def getResults(self):
        """
        @rtype: dict
        @return: the discoAPI results the parse API response
        """
        return self._results
