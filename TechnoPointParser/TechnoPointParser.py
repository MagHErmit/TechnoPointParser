import requests
from bs4 import BeautifulSoup


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

with open('test.txt', 'w', encoding='utf-8') as output_file:
    for s in smart_list:
        output_file.write(s + " ") 