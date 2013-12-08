import discotech

providerConfig = [
    {
        name: 'YouTube',
        url:'http://gdata.youtube.com/feeds/api/videos\
        ?vq=!keyword!&orderby=published&max-results=50\
        &start-index=1'
    },
    {
        name: 'Twitter',
        url: 'https://api.twitter.com/1.1/search/tweets.json\
        ?q=!keyword!&count=100&result_type=recent',
        auth_type_search: 'oauth1',
        auth_value: {
            oauth_client_key: '...',
            oauth_client_secret: '...',
            oauth_token_identifier: '...',
            oauth_token_secret: '...'
}}]


providerSearcher = discotech.ProviderSearcher()

providerSearcher.loadConfig(providerConfig)
