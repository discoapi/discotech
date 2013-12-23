
import json

__package__ = 'discotech.discoAPI'

class ParseResults(object):

    def __init__(self,results):

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
        if self._success != True:
            return False
        if self._nextPageUrl != 'done':
            return True
        else:
            return False

    def nextPageUrl(self):
        return self._nextPageUrl
