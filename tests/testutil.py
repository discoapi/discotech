import json
import os

credentials = {}

def fillUpCredentials(credentials,testCredentials,key):
    if key in testCredentials:
        credentials[key] = testCredentials[key]
    else:
        credentials[key] = ''

#load credentials from json

credentialsFileName = 'testCredentials.json'

# check for cwd
if (os.path.basename(os.getcwd()) != 'tests'):
    credentialsFileName = 'tests/'+credentialsFileName
    

testCredentialsFile = open(credentialsFileName,'r')
testCredentials = json.loads(testCredentialsFile.read())


credentials_values = ['twitter_client_key','twitter_client_secret','twitter_token_identifier',
                      'twitter_token_secret','facebook_access_token','google_access_token',
                      'google_refresh_token','google_token_expire_timestamp','google_client_id',
                      'google_client_secret']


for credentials_value in credentials_values:
    fillUpCredentials(credentials,testCredentials,credentials_value)
    
