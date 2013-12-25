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
            oauth_client_key: 'oP1McZCkEWIP3AxwhMlQQ',
            oauth_client_secret: 'IoVi2pItFoxRDwpy6zijELWZfxD6dLmAbeD8hXD4',
            oauth_token_identifier: '1524406303-dWGaacSBrrKT19aWAUMgkfqMIRu2wejoXnRgqng',
            oauth_token_secret: 'sAna4rv3KuOivgqUMiCTF6oaZyzNSf8JF7p9NU7Ik'
}}]


providerSearcher = discotech.ProviderSearcher()

providerSearcher.loadConfig(providerConfig)

print("end")
