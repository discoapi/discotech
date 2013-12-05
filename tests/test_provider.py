import unittest
import discotech
from discotech import Provider

#requirement for the tes
import time

class TestdiscotechProvider(unittest.TestCase):

    def testConstructor(self):
        # testing with named parametar
        demoProvider = Provider(url = 'http://demourl.com' )
        self.assertEquals(demoProvider.url, 'http://demourl.com', 'wrong url for provider')
        
        #testing without named parametar
        demoProvider = Provider('http://demourl.com' )
        self.assertEquals(demoProvider.url, 'http://demourl.com', 'wrong url for provider')

    def test_none_auth_search(self):
        # query youtube
        youtube = Provider(url = 'http://gdata.youtube.com/feeds/api/videos?vq=!keyword!&orderby=published&max-results=50&start-index=1' )

        results = youtube.search('linux')
        self.assertNotEquals(results, False, 'failed to get results')

    def test_oauth_1_auth_search(self):
        twitter = Provider(url = 'https://api.twitter.com/1.1/search/tweets.json?q=!keyword!&count=100&result_type=recent')

        twitter.setOAuth( clientKey = 'oP1McZCkEWIP3AxwhMlQQ',
                          clientSecret = 'IoVi2pItFoxRDwpy6zijELWZfxD6dLmAbeD8hXD4',
                          tokenIdentifier = '1524406303-dWGaacSBrrKT19aWAUMgkfqMIRu2wejoXnRgqng',
                          tokenSecret = 'sAna4rv3KuOivgqUMiCTF6oaZyzNSf8JF7p9NU7Ik' )

        results = twitter.search('linux')

        self.assertNotEquals(results, False, 'failed to get results')

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
        
        self.assertNotEquals(results, False, 'failed to get results')
        self.assertEqual(tumblr.auth_type_search,'api_key')
        self.assertEqual(tumblr.auth_value['api_key'],'MyAPIKey')


    def test_oauth_2_auth_type_search(self):
        facebook = Provider(url='https://graph.facebook.com/search?q=!keyword!&limit=50&date_format=U&access_token=!oauth2_access_token!')

        facebook.setOAuth2( accessToken='CAACMCfJTFtgBAPO83avt08uAVhwpfwMZApqzFWOWWcnVaW1mOGpVVbc29ZBX2acBcs2Psv3U8CSoJaYwnqfd17zjyrFvXgW0YysWxeDskneSDMZCLYjf4P0ZAQGqWyKzHugwZAxTQpANCK6JKowT0Tt7hYSwRBxV9lGdbimCI0HLAPVgj8oTy' )

        results = facebook.search('linux')
        self.assertNotEquals(results, False, 'failed to get results')


    def test_oauth_2_refresh_token(self):
        googleConfig =  {
            "auth_type_search": "oauth_2",
            "auth_value": {
                "oauth2_access_token": "ya29.1.AADtN_VHmYoL5x3G22evhuSZbLFUqGeBjZ5adHBXixd-R1Dq-5fS9GKQY9u9ZCQ",
                "oauth2_refresh_token": "1/CCByR3P9EDhfP6q4uJzcfcIe4H-ysdKmV2u6jRAP8Dw",
                "oauth2_refresh_token_url": "https://accounts.google.com/o/oauth2/token",
                "oauth2_token_expire_timestamp": 1386159305,
                "oauth2_client_id": "900458772991-t0q31tn75hneirrclt73gjl62o2f2gq3.apps.googleusercontent.com",
                "oauth2_client_secret": "69q4mTtHZXyk0bxrPxlD2yzf"
            },
            "name": "Google+",
            "url": "https://www.googleapis.com/plus/v1/activities?query=!keyword!&maxResults=20&orderBy=recent&access_token=!oauth2_access_token!"
        }

        googlePlus = Provider.initFromDict(googleConfig)

        results = googlePlus.search('linux')
        self.assertNotEquals(results, True, 'failed to get results')

        googlePlus.auth_value['oauth2_access_token'] = 'none'

        googlePlus.refreshOAuth2Token()

        self.assertNotEquals(googlePlus.auth_value['oauth2_access_token'],'none','failed to refresh token')

        #test a forced refresh
        
        googlePlus.auth_value['oauth2_token_expire_timestamp'] = str(int(time.time()) - 100)

        results = googlePlus.search('linux')
        self.assertNotEquals(results, True, 'failed to get results')

        self.assertTrue(googlePlus.auth_value['oauth2_token_expire_timestamp'] > int(time.time()),'failed to to refresh token')
        
        
    def test_isSearchable(self):
        #no auth provider
        noneProvider = Provider('')

        self.assertEquals(noneProvider.isSearchable(),True)

        #OAuth1 provider
        oauth1Provider = Provider('','OAuthProvider','oauth_1')

        self.assertEquals(oauth1Provider.isSearchable(),False)

        #set credentials
        oauth1Provider.setOAuth('','','','')

        self.assertEquals(oauth1Provider.isSearchable(), True)

        #API Key provider
        apikeyProvider = Provider('','APIKeyProvider','api_key')

        self.assertEquals(apikeyProvider.isSearchable(),False)

        #set credentials
        apikeyProvider.setAPIKey('')
        self.assertEquals(apikeyProvider.isSearchable(),True)
        
        
    def test_initFromDict(self):
        
        providerConfig = {
			'name': 'YouTube',
    			'url':'http://gdata.youtube.com/feeds/api/videos?vq=!keyword!&orderby=published&max-results=50&start-index=1'
        }

        youtube = Provider.initFromDict(providerConfig)

        results = youtube.search('linux')

        self.assertNotEquals(results, False, 'failed to get results')

        
if __name__ == '__main__':
    unittest.main()
