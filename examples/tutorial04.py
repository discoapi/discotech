import discotech

providerSearcher = discotech.ProviderSearcher()

providerSearcher.loadConfig('https://discopai.com/api/providers.json')

providerSearcher.getProvider('Twitter').setOAuth(clientKey = '...',
                                          clientSecret = '...',
                                          tokenIdentifier = '...',
                                          tokenSecret = '...' )
  
#let's do a search
results = providerSearcher.search('Twitter','linux')

print(map(lambda(provider): provider.name, providerSearcher.getSearchableProviders()))
#output is :[u'Dailymotion', u'Youtube', u'Metacafe', u'Twitter']

# this will search only dailymotion,youtube,metacafe,twitter
results = providerSearcher.seachAll('linux')

providersConfig = providerSearcher.getConfig()

print(providersConfig)

#notice that twitter's ratelimiting was updated and youtube oauth_type_search was set

#you can easily convert it to JSON for saving
providersConfigJSON = json.dumps(providersConfig)
# but instead you can just save it to file
discotech.saveConfig('myconfig.json')
# notice this will overwrite any previous file content
