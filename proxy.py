import requests
from bs4 import BeautifulSoup

url = "https://www.kuaidaili.com/free/intr/"
res = requests.get(url)
Soup = BeautifulSoup(res.text, 'lxml')
tbody = Soup.find('tbody')
tdlist=Soup.find_all('td',attrs={'data-title':'IP'})
# print(tbody.get_text())
for td in tdlist:
    print(td.get_text())




