# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

user = 'joattt'
url = f'https://api.github.com/users/{user}/repos'
req = requests.get(url)
req_json = req.json()
for repo in req_json:
    print(repo['name'])
with open('repos.json', 'w') as f:
    json.dump(req_json, f)
