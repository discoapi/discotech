import discotech

youtube = discotech.Provider(url = 'http://gdata.youtube.com/feeds/api/videos\
?vq=!keyword!&orderby=published&max-results=50&start-index=1' )

results = youtube.search('linux')

twitter = discotech.Provider(url = 'https://api.twitter.com/1.1/search/tweets.json?q=!keyword!&count=100&result_type=recent')

twitter.setOAuth( clientKey = '...',
                  clientSecret = '...',
                  tokenIdentifier = '...',
                  tokenSecret = '...' )

results = twitter.search('linux')

#notice that the rate limiting was updated
print(vars(twitter))

# saving providers have to set name
youtube.name = 'YouTube'
twitter.name = 'Twitter'

#provider searcher

providerSearcher = discotech.ProviderSearcher()

#add one by one
providerSearcher.addProvider(youtube)
providerSearcher.addProvider(twitter)

#or instead
providerSearcher.addProviders([youtube,twitter])

#now you can search by name
results = providerSearcher.search('YouTube','linux')
results = providerSearcher.search('Twitter','linux')

#notice that the rate limiting was again updated
print(vars(twitter))
  
#or search all
resultsDict = providerSearcher.searchAll('linux')
