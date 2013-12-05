import sys,urllib,unicodedata,time

import requests,requests_oauthlib,json
from requests_oauthlib import OAuth1

from .provider import Provider
from .errors import discotechError
from .ProviderSearcher import ProviderSearcher

#configurable settings
http_timeout_seconds = 20
minimum_rate_limit = 10
debug_string_depth = 100
debug_string_depth_single_provider_method = 10000
provider_tries = 1


#headers for rate limiting
# Instagram, Twitter, Vimeo
rate_limit_headers = {}
# int
rate_limit_headers['hits_remaining'] = ['x-ratelimit-remaining', 'x-rate-limit-remaining', 'x-ratelimit-remaining']
# int (unix_timestamp)
rate_limit_headers['next_window'] = ['INSTAGRAM_FILLER', 'x-rate-limit-reset', 'x-ratelimit-reset']
# int
rate_limit_headers['hits_per_window'] = ['x-ratelimit-limit', 'x-rate-limit-limit', 'x-ratelimit-limit']


def _StrReplaceUrlEnconde(subject, target, replace):
        if (3, 0) <= sys.version_info:
                return subject.replace(target, urllib.parse.quote(replace.encode('utf-8')))
        else:
                return subject.replace(target, urllib.quote(replace.encode('utf-8')))
        

def _provider_query(provider, keyword):        

        #check for rate limits
        if hasattr(provider, 'rl_hits_remaining'):
                if int(provider.rl_hits_remaining) < minimum_rate_limit and int(provider.rl_next_window) > int(time.time()):
                        raise discotechError('rate limit for provider reached')


        #OAuth2 token expire timestamps
        if provider.auth_type_search == 'oauth_2':
                if hasattr(provider.auth_value,'oauth2_token_expire_timestamp'):
                        if 'oauth2_token_expire_timestamp' in provider.auth_value < int(time.time()):
                                if provider.isOAuth2Refreshable():
                                        provider.refreshOAuth2Token()
                                        # check again
                                        if provider.auth_value['oauth2_token_expire_timestamp'] < int(time.time()):
                                                raise discotechError("oauth2 token expire timestamp reached and can't be refreshed")                                          
                       
                                else:
                                        raise discotechError("oauth2 token expire timestamp reached and can't be refreshed")
                                        

        providerUrl = provider.url
        
        if providerUrl==None:
                return False

        #insert keyword to query
        providerUrl = _StrReplaceUrlEnconde(providerUrl, '!keyword!', keyword)
        
        #API Key
        if provider.auth_type_search == 'api_key':
                if hasattr(provider, 'auth_value'):
                      providerUrl = _StrReplaceUrlEnconde(providerUrl, '!api_key!', provider.auth_value['api_key'])  

        #OAuth1
        if provider.auth_type_search == 'oauth_1':
                if hasattr(provider, 'auth_value'):
                        authCredentials = OAuth1(
                                provider.auth_value['oauth_client_key'],
                                provider.auth_value['oauth_client_secret'],
                                provider.auth_value['oauth_token_identifier'],
                                provider.auth_value['oauth_token_secret']
                        )
                else:
                        errorMessage = "Provider requires OAuth Credentials."
                        raise discotechError(errorMessage)
        else:
                authCredentials = {}


        #OAuth2
        if provider.auth_type_search == 'oauth_2':
                if hasattr(provider, 'auth_value'):
                        providerUrl = _StrReplaceUrlEnconde(providerUrl, '!oauth2_access_token!', provider.auth_value['oauth2_access_token'])
                else:
                        errorMessage = "Provider requires OAuth2 Credentials."
                        raise discotechError(errorMessage)                        
                        

        # get Results from provider
        url_contents = getUrlContents(str(providerUrl), '', authCredentials)

        if url_contents['failure_message']!=None:
                return False

        if url_contents['status_code'] != 200:
                # TODO: Handle this!
                pass
                
        data = filterCharacters(url_contents['response_text'])

        #rate limiting
        for key, value in url_contents['headers'].items():
                if key in rate_limit_headers['hits_remaining']:
                        provider.rl_hits_remaining = value
                if key in rate_limit_headers['next_window']:
                        provider.rl_next_window = value
                if key in rate_limit_headers['hits_per_window']:
                        provider.rl_hits_per_window = value
        return data


def getUrlContents(url, postData='', authCredentials={} , headers= None):
        startTime = 0
        endTime = 0
        return_dict = {}
        return_dict['failure_message'] = None
        if headers is None:
                headers = { 'User-Agent' : 'discotech' }

        
        if url=='' or url==None:
                return_dict['failure_message'] = 'NO_URL'
                return return_dict

        if postData=='':
                requestType = 'GET'
                debugMessagePost = ''
        else:
                requestType = 'POST'
        try:
                if postData=='':
                        response = requests.get(url, headers=headers, auth=authCredentials, timeout=http_timeout_seconds, verify=False)
                else:
                        response = requests.post(url, data=postData, headers=headers, auth=authCredentials, timeout=http_timeout_seconds, verify=False)

                        
        except requests.exceptions.ConnectionError as error:
                return_dict['failure_message'] = "Bad internet connection."
                return return_dict

        except Exception as error:
                # Additional errors to catch: http.client.IncompleteRead (Might be able to catch with IncompleteRead)
                # Additional errors to catch: HTTPSConnectionPool, http.client.BadStatusLine
                # Additional errors to catch: requests.exceptions.SSLError (DiscoAPI throws this due to Verification Level 1 cert from StartSSL)

                return_dict['failure_message'] = str(error)

                errorMessage = "\ngetUrlContents("+requestType+"): The following error occurred: " + str(error)
                errorMessage+= "\nURL: " + url

                if not postData=='':
                        for key,value in postData.items():
                                try:
                                        final_value = zlib.decompress(value)
                                except zlib.error:
                                        final_value = value
                                errorMessage += "\nPOST " + key + ": " + str(final_value[0:debug_string_depth])

                try:
                        errorMessage+= "\nResponse Code: " + str(response.status_code)
                        errorMessage+= "\nResponse Headers: " + str(response.headers)
                        errorMessage+= "\nResponse Text: " + str(response.text)
                except:
                        errorMessage+= "\nCannot add Response Code/Headers/Text."

                return return_dict


        return_dict['response_text'] = response.text
        return_dict['status_code'] = response.status_code
        return_dict['headers'] = response.headers
        return_dict['totalRequestTime'] = endTime-startTime

        return return_dict



def filterCharacters(s):
        """
        Strip non printable characters

        @version 2013-07-19

        @type  s dict|list|tuple|bytes|string
        @param s Object to remove non-printable characters from

        @rtype  dict|list|tuple|bytes|string
        @return An object that corresponds with the original object, nonprintable characters removed.
        """

        validCategories = ('Lu', 'Ll', 'Lt', 'LC', 'Lm', 'Lo', 'L', 'Mn', 'Mc', 'Me', 'M', 'Nd', 'Nl', 'No', 'N', 'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po', 'P', 'Sm', 'Sc', 'Sk', 'So', 'S', 'Zs', 'Zl', 'Zp', 'Z')
        convertToBytes = False

        if isinstance(s, dict):
                new = {}
                for k,v in s.items():
                        new[k] = filterCharacters(v)
                return new

        if isinstance(s, list):
                new = []
                for item in s:
                        new.append(filterCharacters(item))
                return new

        if isinstance(s, tuple):
                new = []
                for item in s:
                        new.append(filterCharacters(item))
                return tuple(new)

        if (3, 0) <= sys.version_info:
                if isinstance(s, bytes):
                        s = s.decode('utf-8')
                        convertToBytes = True

                if isinstance(s, str):
                        s = ''.join(c for c in s if unicodedata.category(c) in validCategories)
                        if convertToBytes:
                                s = s.encode('utf-8')
                        return s
                else:
                        return None

        else:
                if isinstance(s, str):
                        s = s.decode('utf-8')
                        convertToBytes = True

                if isinstance(s, unicode):
                        s = ''.join(c for c in s if unicodedata.category(c) in validCategories)
                        if convertToBytes:
                                s = s.encode('utf-8')
                        return s
                else:
                        return None



def refresh_OAuth2_Token(self):
        if self.auth_type_search != 'oauth_2':
            raise discotechError('Not a OAuth2 provider')

        #prepare refresh token fields

        postFields = {
            'refresh_token' : self.auth_value['oauth2_refresh_token'],
            'client_id' : self.auth_value['oauth2_client_id'],
            'client_secret' : self.auth_value['oauth2_client_secret'],
            'grant_type' : 'refresh_token'
        }
        
        encodedpostField = urllib.urlencode(postFields)

        newToken = getUrlContents(self.auth_value['oauth2_refresh_token_url'],encodedpostField,
                                  {},{'Content-Type': 'application/x-www-form-urlencoded'})
        
        #parse the response, this works only with google
        newToken = json.loads(newToken['response_text'])

        self.auth_value['oauth2_access_token'] = newToken['access_token']
        self.auth_value['oauth2_token_expire_timestamp'] = int(time.time()) + newToken['expires_in']

# dynamiclly add refresh token
Provider.refreshOAuth2Token = refresh_OAuth2_Token


# dynamiclly add search function to Provider class
def provider_search(self,keyword):
        return _provider_query(self,keyword)

Provider.search = provider_search


