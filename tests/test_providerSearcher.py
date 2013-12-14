import unittest
import discotech
import json
import testutil
import os
import sys
import random

class TestProviderSeacher(unittest.TestCase):


    # utility filterning for configs
    def _createNameComprator(self,name):
        return lambda provider: True if provider['name'] == name else False
                               
    
    def setUp(self):
        self.providerSearcher = discotech.ProviderSearcher()
        # every test the discotech module should be reloaded because it has a saved state
        #reload(discotech)
        

    def test_addProvider(self):
        unnamedProvider = discotech.Provider('...')


        
        
        # missing
        if (3, 2) <= sys.version_info:
            with self.assertRaisesRegex(discotech.discotechError,'Missing name for provider'):
                self.providerSearcher.addProvider(unnamedProvider)
        else:
            with self.assertRaisesRegexp(discotech.discotechError,'Missing name for provider'):
                self.providerSearcher.addProvider(unnamedProvider)
        #give it a name
        unnamedProvider.name = 'named provider'
        namedProvider = unnamedProvider
        
        self.providerSearcher.addProvider(namedProvider)
        

    def test_search(self):
        providerConfig = {
                        'name': 'YouTube',
                        'url':'http://gdata.youtube.com/feeds/api/videos?vq=!keyword!&orderby=published&max-results=50&start-index=1'
        }

        youtube = discotech.Provider.initFromDict(providerConfig)
        self.providerSearcher.addProvider(youtube)
        
        results = self.providerSearcher.search('YouTube','linux')

        self.assertNotEqual(results,False)
        # try unknown provider

        if (3, 2) <= sys.version_info:
            with self.assertRaisesRegex(discotech.discotechError,'Unknown Provider'):
                results = self.providerSearcher.search('Unknown Provider','linux')
        else:
            with self.assertRaisesRegexp(discotech.discotechError,'Unknown Provider'):
                results = self.providerSearcher.search('Unknown Provider','linux')

    def test_searchAll(self):
        providerConfig = {
            'name': 'YouTube',
            'url': 'http://gdata.youtube.com/feeds/api/videos?vq=!keyword!&orderby=published&max-results=50&start-index=1'
        }

        self.providerSearcher.addProvider(discotech.Provider.initFromDict(providerConfig))

        providerConfig = {
            'name': 'Metacafe',
            'url' : 'http://metacafe.com/api/videos/?vq=!keyword!&max-results=50&time=all_tume&orderby=updated&start-index=1'
        }

        self.providerSearcher.addProvider(discotech.Provider.initFromDict(providerConfig))

        results = self.providerSearcher.searchAll('linux')

        #make sure we have only results from providers we put in
        self.assertIn('YouTube',results)
        self.assertIn('Metacafe',results)

        
    def test_loadConfig(self):
        providerConfig = [
            {'name': 'YouTube',
             'url': 'http://gdata.youtube.com/feeds/api/videos?vq=!keyword!&orderby=published&max-results=50&start-index=1'
            },
            {'name': 'Metacafe',
             'url' : 'http://metacafe.com/api/videos/?vq=!keyword!&max-results=50&time=all_tume&orderby=updated&start-index=1'
             }]

        self.providerSearcher.loadConfig(providerConfig)

        results = self.providerSearcher.searchAll('linux')

        #make sure we have only results from providers we put in
        self.assertIn('YouTube',results)
        self.assertIn('Metacafe',results)
  
    def test_getConfig(self):
        self.assertEqual(self.providerSearcher.getConfig(),[])

        providerConfig = [
            {'name': 'YouTube',
             'url': 'http://gdata.youtube.com/feeds/api/videos?vq=!keyword!&orderby=published&max-results=50&start-index=1'
            },
            {'name': 'Metacafe',
             'url' : 'http://metacafe.com/api/videos/?vq=!keyword!&max-results=50&time=all_tume&orderby=updated&start-index=1'
             }]

        self.providerSearcher.loadConfig(providerConfig)

        myConfig = self.providerSearcher.getConfig()
             
        #we want to check that at least one of the providers have the named we sent
        self.assertEqual(len(list(filter(self._createNameComprator('YouTube'),myConfig))),1)

        #let's check the other one
        self.assertEqual(len(list(filter(self._createNameComprator('Metacafe'),myConfig))),1)

        #we got only 2 providers
        self.assertEqual(len(myConfig),2)

        
    def test_loadBaseConfig(self):
        self.assertEqual(self.providerSearcher.getConfig(),[])

        providerConfig = [
            {'name': 'YouTube',
             'url': 'http://gdata.youtube.com/feeds/api/videos?vq=!keyword!&orderby=published&max-results=50&start-index=1',
             'auth_type_search': 'none'
            },
            {'name': 'Metacafe',
             'url' : 'http://metacafe.com/api/videos/?vq=!keyword!&max-results=50&time=all_tume&orderby=updated&start-index=1',
             'auth_type_search': 'none'
             }]

        self.providerSearcher.loadBaseConfig(providerConfig)

        self.assertEqual(self.providerSearcher.getConfig(),[])


        
        #another scenario

        self.providerSearcher = discotech.ProviderSearcher()
        
        self.assertEqual(self.providerSearcher.getConfig(),[])
        
        baseProviderConfig = [
            {'name': 'YouTube',
             'url': 'http://gdata.youtube.com/feeds/api/videos?vq=!keyword!&orderby=published&max-results=50&start-index=1',
             'auth_type_search': 'none'
            },
            {'name': 'Facebook',
             'url' : 'https://graph.facebook.com/search?q=!keyword!&limit=50&date_format=U&access_token=!oauth2_access_token!'
         }]

        providerConfig = {
            'name': 'Metacafe',
            'url': 'http://metacafe.com/api/videos/?vq=!keyword!&max-results=50&time=all_tume&orderby=updated&start-index=1',
            'auth_type_search': 'none'
        }

        
        self.providerSearcher.loadBaseConfig(baseProviderConfig)
        self.providerSearcher.loadConfig(providerConfig)

        #configure another provider
        self.providerSearcher.getProvider('Facebook').setOAuth2( accessToken= testutil.credentials['facebook_access_token'] )

        myConfig = self.providerSearcher.getConfig()

        #doesn't have YouTube config
        self.assertEqual(len(list(filter(self._createNameComprator('YouTube'),myConfig))),0)
        
        #facebook has only auth_value and type
        facebookConfig = list(filter(self._createNameComprator('Facebook'),myConfig))[0]

        self.assertTrue('auth_value' in facebookConfig)
        self.assertTrue('auth_type_search' in facebookConfig)

        self.assertEqual(len(facebookConfig.items()),3)
        
        #metacafe is saved
        self.assertEqual(len(list(filter(self._createNameComprator('Metacafe'),myConfig))),1)
        
        # only 2 providers in config
        self.assertEqual(len(myConfig),2)
        

        
    def test_saveConfig(self):

        #continue from prevous test
        self.test_loadBaseConfig()

        #create random file name
        fileName = 'temp'+str(int(random.random()*10000))+'.json'

        newFileNameFound = False
        while not newFileNameFound:
            #create random file name
            fileName = 'temp'+str(int(random.random()*10000))+'.json'
            if not os.path.exists(fileName):
                newFileNameFound = True
        
        #save the config
        self.providerSearcher.saveConfig(fileName)
        
        # load the json file manually
        jsonFile = open(fileName,'r')

        #compare the json and the dict
        self.assertEqual(json.loads(jsonFile.read()),self.providerSearcher.getConfig())

        jsonFile.close()
        #cleanup - delete this file
        os.remove(fileName)
if __name__ == '__main__':
    unittest.main()
