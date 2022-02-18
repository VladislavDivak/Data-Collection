#curl -u VladislavDivak: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 -H "Accept: application/vnd.github.v3+json" https://api.github.com/octocat/repos

import requests
import json
from pprint import pprint

url = 'https://api.github.com/users/'
user = 'octocat'
#enter_user = 'xxxxxxx' #in case you need authorisation
#token = 'xxxxxxx' #in case you need authorisation, token with expiration date
accept = 'application/vnd.github.v3+json'
visibility = 'public'
params = {#enter_user: token, #in case you need authorisation
          'accept': accept,
          'visibility': visibility}

response = requests.get(url+user+'/repos', params=params)

j_data = response.json()

#pprint(j_data)
print(f'User {j_data[0].get("owner").get("login")} has {len(j_data)} repositories on GitHub. Here they are:')
for i in j_data:
    print(i.get("name"))

json_data = {'repos': j_data}
with open('homework_lesson1.json', 'w') as outfile:
    json.dump(json_data, outfile)



