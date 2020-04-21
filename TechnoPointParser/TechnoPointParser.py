import requests
from bs4 import BeautifulSoup
import json

url = 'https://technopoint.ru/catalog/recipe/e351231ca6161134/2020-goda/'

s = requests.Session()
s.headers.update({
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130'
    })
r = s.get(url)

soup = BeautifulSoup(r.text, features="lxml")
list_products = soup.find_all('div', {'class' : 'catalog-item'})


names = []
numbers = []
links = []
price = []

data = {"data":"{\"type\":\"price\",\"containers\":["}

for i in range (0,10):
    names.append(list_products[i].find('div', {'class': 'product-info__title-link'}).find('a').text)
    numbers.append(list_products[i].find('span', {'data-product-param' : 'code'}).text)
    links.append(list_products[i].find('img').get('data-src'))
    data['data'] += "{\"id\":\"not-empty-%i\",\"data\":{\"product\":\"%s\"}}," % (i, list_products[i].get('data-guid'))

data['data'] = data['data'][:-1]
data['data'] += "]}"
    

results = {
           'names' : names,
           'numbers' : numbers,
           'links' : links,
           'price' : price
          }



token = soup.find('meta', {'name' : 'csrf-token'}).get('content')

s.headers.update({
    'x-csrf-token' : token,
    'origin' : 'https://technopoint.ru',
    'referer' : 'https://technopoint.ru/catalog/recipe/e351231ca6161134/2020-goda/no-referrer',
    'sec-fetch-mode' : 'cors',
    'content-type' : 'application/x-www-form-urlencoded',
    'x-requested-with' : 'XMLHttpRequest',
    })



ans = json.loads(s.post('https://technopoint.ru/ajax-state/price/', data = data).text)

for price in ans['data']['states']:
    results['price'].append(price['data']['current'])

