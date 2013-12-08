import discotech

providerSearcher = discotech.ProviderSearcher()

providerSearcher.loadBaseConfig('https://discoapi.com/api/providers.json')
providerSearcher.loadConfig('myCredentials.json')

results = providerSearcher.search('Twitter','linux')

providerSearcher.saveConfig('myCredentials.json')
