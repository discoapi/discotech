import unittest
import discotech
from discotech import Provider
#requirement for the test
import time

#test utilities
import testutil

class TestdiscotechProvider(unittest.TestCase):

    def testConstructor(self):
        # testing with named parametar
        demoProvider = Provider(url = 'http://demourl.com' )
        self.assertEqual(demoProvider.url, 'http://demourl.com', 'wrong url for provider')
        
        #testing without named parametar
        demoProvider = Provider('http://demourl.com' )
        self.assertEqual(demoProvider.url, 'http://demourl.com', 'wrong url for provider')

    def test_none_auth_search(self):
        # query youtube
        youtube = Provider(url = 'http://gdata.youtube.com/feeds/api/videos?vq=!keyword!&orderby=published&max-results=50&start-index=1' )

        results = youtube.search('linux')
        self.assertNotEqual(results, False, 'failed to get results')

    def test_oauth_1_auth_search(self):
        twitter = Provider(url = 'https://api.twitter.com/1.1/search/tweets.json?q=!keyword!&count=100&result_type=recent')

        twitter.setOAuth( clientKey = testutil.credentials['twitter_client_key'],
                          clientSecret = testutil.credentials['twitter_client_secret'],
                          tokenIdentifier = testutil.credentials['twitter_token_identifier'],
                          tokenSecret = testutil.credentials['twitter_token_secret'] )

        results = twitter.search('linux')

        self.assertNotEqual(results, False, 'failed to get results')

    def test_ratelimitint(self):

        conf = {
            'url': 'none',
            'rl_hits_remaining' : str(0),
            'rl_next_window': str(int(time.time()) + 3600) #next hour
        }

        badProvider = Provider.initFromDict(conf)

        with self.assertRaises(discotech.discotechError):
            badProvider.search('linux')

        
    def test_apikey_auth_type_search(self):
        tumblr = Provider('http://api.tumblr.com/v2/tagged?tag=!keyword!&format=text&limit=20&api_key=!api_key!')
        tumblr.setAPIKey('MyAPIKey')
        results = tumblr.search('linux')
        
        self.assertNotEqual(results, False, 'failed to get results')
        self.assertEqual(tumblr.auth_type_search,'api_key')
        self.assertEqual(tumblr.auth_value['api_key'],'MyAPIKey')


    def test_oauth_2_auth_type_search(self):
        facebook = Provider(url='https://graph.facebook.com/search?q=!keyword!&limit=50&date_format=U&access_token=!oauth2_access_token!')

        facebook.setOAuth2( accessToken=testutil.credentials['facebook_access_token'] )

        results = facebook.search('linux')
        self.assertNotEqual(results, False, 'failed to get results')


    def test_oauth_2_refresh_token(self):
        googleConfig =  {
            "auth_type_search": "oauth_2",
            "auth_value": {
                "oauth2_access_token": testutil.credentials['google_access_token'],
                "oauth2_refresh_token": testutil.credentials['google_refresh_token'],
                "oauth2_refresh_token_url": "https://accounts.google.com/o/oauth2/token",
                "oauth2_token_expire_timestamp": testutil.credentials['google_token_expire_timestamp'],
                "oauth2_client_id": testutil.credentials['google_client_id'],
                "oauth2_client_secret": testutil.credentials['google_client_secret']
            },
            "name": "Google+",
            "url": "https://www.googleapis.com/plus/v1/activities?query=!keyword!&maxResults=20&orderBy=recent&access_token=!oauth2_access_token!"
        }

        googlePlus = Provider.initFromDict(googleConfig)

        results = googlePlus.search('linux')
        self.assertNotEqual(results, True, 'failed to get results')

        googlePlus.auth_value['oauth2_access_token'] = 'none'

        googlePlus.refreshOAuth2Token()

        self.assertNotEqual(googlePlus.auth_value['oauth2_access_token'],'none','failed to refresh token')

        #test a forced refresh
        
        googlePlus.auth_value['oauth2_token_expire_timestamp'] = (int(time.time()) - 100)

        results = googlePlus.search('linux')
        self.assertNotEqual(results, True, 'failed to get results')

        self.assertTrue(googlePlus.auth_value['oauth2_token_expire_timestamp'] > int(time.time()),'failed to to refresh token')
        
        
    def test_isSearchable(self):
        #no auth provider
        noneProvider = Provider('')

        self.assertEqual(noneProvider.isSearchable(),True)

        #OAuth1 provider
        oauth1Provider = Provider('','OAuthProvider','oauth_1')

        self.assertEqual(oauth1Provider.isSearchable(),False)

        #set credentials
        oauth1Provider.setOAuth('','','','')

        self.assertEqual(oauth1Provider.isSearchable(), True)

        #API Key provider
        apikeyProvider = Provider('','APIKeyProvider','api_key')

        self.assertEqual(apikeyProvider.isSearchable(),False)

        #set credentials
        apikeyProvider.setAPIKey('')
        self.assertEqual(apikeyProvider.isSearchable(),True)
        
        
    def test_initFromDict(self):
        
        providerConfig = {
			'name': 'YouTube',
    			'url':'http://gdata.youtube.com/feeds/api/videos?vq=!keyword!&orderby=published&max-results=50&start-index=1'
        }

        youtube = Provider.initFromDict(providerConfig)

        results = youtube.search('linux')

        self.assertNotEqual(results, False, 'failed to get results')

        
if __name__ == '__main__':
    unittest.main()
