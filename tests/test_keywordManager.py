import unittest
from discotech import KeywordManager

class TestKeywordManager(unittest.TestCase):

    
    def testConstructor(self):

	keywordManager = KeywordManager()
	self.assertEqual(keywordManager.keywords,[],"keywords should be empty")

	testValues = ['stas','hagit','love']
	keywordManager = KeywordManager(['stas','hagit','love'])
	self.assertEqual(keywordManager.keywords,testValues)
	testValues.remove('stas')
	self.assertNotEqual(keywordManager.keywords,testValues)

    def test_dequeue(self):

	testValues = ['stas','hagit','love']

	keywordManager = KeywordManager(testValues)

	# do three rounds of tests
	for i in range(3):
	    for testValue  in testValues:
		value = keywordManager.dequque()
		self.assertEqual(value,testValue)

	#check again

	self.assertEqual(keywordManager.dequque(),'stas')
	
if __name__ == '__main__':
    unittest.main()
