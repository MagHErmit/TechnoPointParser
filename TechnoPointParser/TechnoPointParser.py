import requests
from bs4 import BeautifulSoup
import json

s = requests.Session()
s.headers.update({
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130'
    })
url = 'https://technopoint.ru/catalog/recipe/e351231ca6161134/2020-goda/'
r = s.get(url)

soup = BeautifulSoup(r.text, features="lxml")
smart_list = []
list_names = soup.find_all('div', {'class': 'product-info__title-link'})
for item in list_names:
    name = item.find('a').text
    smart_list.append(name)


token = soup.find('meta', {'name' : 'csrf-token'}).get('content')

sp = requests.Session();
headerss = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130',
    'x-csrf-token' : token,
    'origin' : 'https://technopoint.ru',
    'referer' : 'https://technopoint.ru/catalog/recipe/e351231ca6161134/2020-goda/no-referrer',
    'sec-fetch-mode' : 'cors',
    'content-type' : 'application/x-www-form-urlencoded',
    'x-requested-with' : 'XMLHttpRequest',
    'accept': '*/*'
    }
data = {"data":"{\"type\":\"price\",\"containers\":[{\"id\":\"ajs-03af27f5-3f0a-4e98-af5c-0813b0aaf96e\",\"data\":{\"product\":\"54ce082a-35c3-11ea-a20d-00155d03332b\"}},{\"id\":\"ajs-801afd81-c945-45e4-9886-a4ac0d147526\",\"data\":{\"product\":\"11208c6a-35c3-11ea-a20d-00155d03332b\"}},{\"id\":\"ajs-a68f1213-c9bc-4d49-bd02-d8b9c6253f4a\",\"data\":{\"product\":\"a185ca45-35c2-11ea-a20d-00155d03332b\"}},{\"id\":\"ajs-aaa13b89-fa41-49d8-b6bf-47a4e97db674\",\"data\":{\"product\":\"0c0eac7d-40c6-11ea-a20f-00155d03332b\"}},{\"id\":\"ajs-2f480072-1655-4f50-88a7-ec36b9b15e52\",\"data\":{\"product\":\"de47f9f8-40c5-11ea-a20f-00155d03332b\"}},{\"id\":\"ajs-17696d6a-32f4-4788-9afb-cddf1c76c024\",\"data\":{\"product\":\"761ae482-628f-11ea-a20f-00155d03332b\"}},{\"id\":\"ajs-45b2cd9a-79e8-461c-84b0-5c797e49b9f6\",\"data\":{\"product\":\"a8f3ed46-628f-11ea-a20f-00155d03332b\"}},{\"id\":\"ajs-22c39cbd-9b46-4c6f-8f53-13e3466eaedd\",\"data\":{\"product\":\"3c9139ac-628f-11ea-a20f-00155d03332b\"}},{\"id\":\"ajs-70176d5d-f94c-4291-a4a3-389b9ad72844\",\"data\":{\"product\":\"11357834-5909-11ea-a20f-00155d03332b\"}},{\"id\":\"ajs-9266c1ab-8b42-4b01-bd55-a985fed88c38\",\"data\":{\"product\":\"f382901c-5908-11ea-a20f-00155d03332b\"}},{\"id\":\"ajs-fa43077f-6396-49ad-8475-31c395b09525\",\"data\":{\"product\":\"d51f56a5-374e-11ea-a20d-00155d03332b\"}},{\"id\":\"ajs-a887ce7c-a478-40c1-9331-13f49f3f6495\",\"data\":{\"product\":\"7d7d4f79-374f-11ea-a20d-00155d03332b\"}},{\"id\":\"ajs-d3f9a796-1b81-4397-a4d1-f8ce3793131e\",\"data\":{\"product\":\"b9b3c23e-374e-11ea-a20d-00155d03332b\"}},{\"id\":\"ajs-14e0459d-a0f0-4779-ae5d-85e338a62763\",\"data\":{\"product\":\"610e037d-374e-11ea-a20d-00155d03332b\"}},{\"id\":\"ajs-0a58db05-919b-457c-9278-8af8a248865d\",\"data\":{\"product\":\"5bfc7f58-3b40-11ea-a20c-00155df1b805\"}},{\"id\":\"ajs-6de50572-5113-44fc-8641-6bb181e0e4cf\",\"data\":{\"product\":\"6e6e0210-3b3d-11ea-a20c-00155df1b805\"}},{\"id\":\"ajs-5610d043-7201-41ae-820a-fb9e954b7c54\",\"data\":{\"product\":\"c9c4bc44-3b3f-11ea-a20c-00155df1b805\"}},{\"id\":\"ajs-451d64ab-496c-405e-9a88-7d3be094c432\",\"data\":{\"product\":\"21b015ce-38f9-11ea-a20d-00155d03332b\"}}]}"}

ans = json.loads(s.post('https://technopoint.ru/ajax-state/price/', headers = headerss, data = data).text)

for price in ans['data']['states']:
    print(price['data']['current'])

with open('test.txt', 'w', encoding='utf-8') as output_file:
    for s in smart_list:
        output_file.write(s + " ") 
