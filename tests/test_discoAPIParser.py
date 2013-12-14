import unittest
from discotech import DiscoAPIParser
import discotech

import sys

#test utilities
import testutil


class TestDiscoAPIParser(unittest.TestCase):

    def test_parse(self):

	discoAPIParser = DiscoAPIParser()
	# missing api key
        if (3, 2) <= sys.version_info:
            with self.assertRaisesRegex(discotech.discotechError,'api key'):
                discoAPIParser.parse("","twitter","keyword")
        else:
            with self.assertRaisesRegexp(discotech.discotechError,'api key'):
                discoAPIParser.parse("","twitter","keyword")	

	#set discoAPI key
	discoAPIParser.setDiscoAPIKey(testutil.credentials['discoAPI_key'])
		
	providerSearcher = discotech.ProviderSearcher()
	providerSearcher.loadConfig('https://discoapi.com/api/providers.json')

	results = providerSearcher.search('Youtube','linux')

	parseResults = discoAPIParser.parse(results,'youtube','linux')

	self.assertNotEqual(parseResults,None)
	self.assertTrue(parseResults.hasMorePages())
	
if __name__ == '__main__':
    unittest.main()
    
