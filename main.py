from meizituQueue import MeizituQueue
from download import request
from bs4 import BeautifulSoup

spider_queue = MeizituQueue('meizitu', 'title_queue')


def start(url):
    response = request.get(url,3)
    soup = BeautifulSoup(response.text, 'lxml')
    all_a = soup.find('div', class_='all').find_all('a')
    for a in all_a:
        title = a.get_text()
        url = a['href']
        print('push '+url)
        spider_queue.push(url, title)


if __name__ == "__main__":
    start('http://www.mzitu.com/all')
