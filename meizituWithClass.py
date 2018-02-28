import requests
from bs4 import BeautifulSoup
import os
import pymongo
from pymongo import MongoClient
from download import request
import datetime

config = {'headers': {},
          'start_url': ''
          }


class Meizitu:
    def __init__(self):
        client = MongoClient()
        db = client['meizitu']
        self.meizitu_collection = db['meizitu_image']
        self.headers = config['headers']

        self.title = ''
        self.url = ''
        self.img_urls = []

    def all_url(self, url):
        response = request.get(url, 3)
        all_a = BeautifulSoup(response.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            self.title = title
            path = os.path.join("/Users/fanzixiao/PycharmProjects/meizitu/image", title)
            self.mkdir(path)
            os.chdir(path)
            href = a['href']
            self.url = href
            if not self.meizitu_collection.find_one({'title_url': href}):
                self.html(self.url)

    def html(self, url):
        html = request.get(url, 5)

        print(url)
        div_pagenavi = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi')
        if div_pagenavi is not None:
            max_span = div_pagenavi.find_all('span')[-2].get_text()
            self.headers['Referer'] = url
            for page_num in range(1, int(max_span) + 1):
                page_url = url + '/' + str(page_num)
                self.getImg(page_url, max_span, page_num)

    def getImg(self, page_url, max_span, page_num):
        img_html = request.get(page_url, 3)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.img_urls.append(img_url)
        if (int(max_span) == page_num):
            self.save(img_url)
            post = {
                'title': self.title,
                'title_url': self.url,
                'image_urls': self.img_urls,
                'get_time': datetime.datetime.now()
            }
            self.meizitu_collection.save(post)
        else:
            self.save(img_url)

    def save(self, img_url):
        name = img_url[-9:-4]
        img = request.get(img_url, 3, headers=self.headers)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path):
        path = str(path).strip()
        isExist = os.path.exists(path)
        if isExist:
            return False
        else:
            os.mkdir(path)


meizitu = Meizitu()
meizitu.all_url('http://www.mzitu.com/all')
