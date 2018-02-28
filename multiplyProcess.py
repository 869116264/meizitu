import os
import time
import threading
import multiprocessing
from meizituQueue import MeizituQueue
from download import request
from bs4 import BeautifulSoup

SLEEP_TIME = 1


def meizitu_crawler(max_thread, lock):
    crawler_queue = MeizituQueue('meizitu', 'title_queue')
    headers = {}

    def pageurl_crawler(lock):
        while True:
            try:
                title_url = crawler_queue.pop()
                print('title_url is', title_url)
            except KeyError:
                print(KeyError)
                break
            else:
                img_urls = []
                response = request.get(title_url, 3)
                title = crawler_queue.pop_title(title_url)
                print('title is ', title)
                mkdir(title)
                div_pagenavi = BeautifulSoup(response.text, 'lxml').find('div', class_='pagenavi')
                if div_pagenavi is not None:
                    max_span = div_pagenavi.find_all('span')[-2].get_text()
                    headers['Referer'] = title_url
                    for page_num in range(1, int(max_span) + 1):
                        page_url = title_url + '/' + str(page_num)
                        print('page_url is', page_url)
                        html = request.get(page_url, 3)
                        img_url = ''
                        img_main = \
                            BeautifulSoup(html.text, 'lxml').find('div', class_='main-image')
                        if img_main:
                            img_url = img_main.find(
                                'img')[
                                'src']
                        img_urls.append(img_url)
                        # os.chdir(os.path.join("/Users/fanzixiao/PycharmProjects/meizitu/image", title))
                        save(img_url, os.path.join("/Users/fanzixiao/PycharmProjects/meizitu/image", title), lock)
                        # print('save',img_url)
                        # print(os.getcwd())
                    crawler_queue.complete(title_url)

    def mkdir(path):
        path = str(path).strip()
        path = os.path.join("/Users/fanzixiao/PycharmProjects/meizitu/image", path)
        isExist = os.path.exists(path)
        if isExist:
            return False
        else:
            os.mkdir(path)

    def save(img_url, path, lock):
        name = img_url[-9:-4]
        img = request.get(img_url, 3, headers=headers)
        lock.acquire()
        os.chdir(path)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()
        lock.release()

    threads = []
    while threads or crawler_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_thread or crawler_queue.peek():
            thread = threading.Thread(target=pageurl_crawler, args=(lock,))
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)


def process_crawler():
    # print('123')
    path = "/Users/fanzixiao/PycharmProjects/meizitu/image"
    isExist = os.path.exists(path)
    if not isExist:
        os.mkdir(path)

    lock = multiprocessing.Lock()
    processes = []
    # num = multiprocessing.cpu_count()
    num = 4
    print('cpu num is' + str(num))
    for i in range(num):
        p = multiprocessing.Process(target=meizitu_crawler, args=(1, lock))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


if __name__ == '__main__':
    process_crawler()
