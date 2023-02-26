# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее
# авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

service = 'https://samples.openweathermap.org/data/2.5/weather'
appid = 'b6907d289e10d714a6e88b30761fae22'
city = 'London,uk'
url = f'{service}?q={city}&appid={appid}'
req = requests.get(url)
req_json = req.json()
print(req_json)
with open('weather.json', 'w') as f:
    json.dump(req_json, f)
