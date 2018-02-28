import requests
from bs4 import BeautifulSoup
import os

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
}
all_url = 'http://www.mzitu.com/all'
start_html = requests.get(all_url, headers=headers)
print(start_html.text)
print(type(start_html))
# print(start_html.raise_for_status())
# print(start_html.text)
Soup = BeautifulSoup(start_html.text, 'lxml')
print(type(Soup))

a_list = Soup.find('div', class_='all').find_all('a')
print(type(a_list))
exit()
# os.mkdir("/Users/fanzixiao/PycharmProjects/meizitu/image2")
# os.chdir("/Users/fanzixiao/PycharmProjects/meizitu/image2")
for a in a_list:
    title = a.get_text()
    path = str(title).strip()
    os.mkdir(os.path.join("/Users/fanzixiao/PycharmProjects/meizitu/test2", path))
    os.chdir(os.path.join("/Users/fanzixiao/PycharmProjects/meizitu/test2",path))
    # print('切换完毕')
    href = a['href']
    html = requests.get(href, headers=headers)
    html_soup = BeautifulSoup(html.text, 'lxml')
    div_pagenavi = html_soup.find('div', class_='pagenavi')
    headers['Referer'] = href
    if not div_pagenavi is None:
        max_span = div_pagenavi.find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            # print(page_url)
            # print(headers)
            img_html = requests.get(page_url, headers=headers)
            img_soup = BeautifulSoup(img_html.text, 'lxml')
            img_main = img_soup.find('div', class_='main-image')
            if img_main:
                img_url = img_main.find('img')['src']
                img_name = img_url[-9:-4]
                img = requests.get(img_url, headers=headers)
                f = open(img_name + '.jpg', 'ab')
                f.write(img.content)
                f.close()
                # print(img_url)
    else:
        print('error response 514')  # get不到的页面

    # max_span = html_soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
    # for page in range(1, int(max_span) + 1):
    #     page_url = href + '/' + page
