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
    

results = [
           names,
           numbers,
           price,
           links
          ]



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
    results[2].append(price['data']['current'])


##################-----------------------WRITE TO EXCEL TABLE-----------------------##################

from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, Side

fill = PatternFill(fill_type='solid',start_color='FFD700')
font = Font(name='Calibri',
                    bold=True,
                    )


wb = Workbook()
ws = wb.active
ws.title = 'Смартфоны 2020'
topic = ['Наименование', 'Код товара', 'Цена', 'Ссылка на изображение']
#for row in topic:
ws.append(topic)

for cellObj in ws['A1:D1']:
    for cell in cellObj:
        cell.fill = fill
        cell.font = font
for i in range(0,10):
    row = []
    for j in range(0,4):
        row.append(results[j][i])
    ws.append(row)

dims = {}
for row in ws.rows:
    for cell in row:
        if cell.value:
            dims[cell.column_letter] = max((dims.get(cell.column, 0), len(cell.value)))
for col, value in dims.items():
    ws.column_dimensions[col].width = value + 1
 
wb.save('Смартфоны.xlsx')