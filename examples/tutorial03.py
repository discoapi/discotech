import discotech

providerSearcher = discotech.ProviderSearcher()

providerSearcher.loadConfig('providers.json')
providerSearcher.loadConfig('https://discopai.com/api/providers.json')
