import requests
import re
import random
import time
from bs4 import BeautifulSoup


class download:
    def __init__(self):
        self.__user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

        # self.__user_IP_list = self.__initIPList("https://www.kuaidaili.com/free/intr/")

    def get(self, url, timeout, proxy=None, num_retries=0, headers={}):
        print('开始get:',url)
        if not url == '':
            user_agent = random.choice(self.__user_agent_list)
            headers['User-Agent'] = user_agent
            response = requests.get(url, headers=headers)
            return response
        # if proxy == None:
        #     try:
        #         response = requests.get(url, headers=headers)
        #         return response
        #     except:
        #         if num_retries > 0:
        #             # time.sleep(2)
        #             print(u'获取网页出错,将获取倒数第', num_retries, '次')
        #             return self.get(url, timeout, num_retries=num_retries - 1)
        #         else:
        #             print('开始使用代理')
        #             return self.get(url, timeout, num_retries=num_retries - 1, proxy=True)
        # else:
        #     try:
        #         IP = random.choice(self.__ipList)
        #         proxy = {'http': IP}
        #         # print(proxy)
        #         response = requests.get(url, headers=headers, timeout=timeout, proxies=proxy)
        #         return response
        #     except:
        #         if (num_retries > 0):
        #             print('切换代理,当前代理为', proxy, ',该代理已失效.仍要切换', num_retries, '次')
        #             return self.get(url, timeout, proxy, num_retries - 1)
        #         else:
        #             print('代理切换次数用完,取消代理')
        #             return self.get(url, timeout)

    def __initIPList(self, url, xml_type='lxml'):
        self.__ipList = []
        res = requests.get(url)
        Soup = BeautifulSoup(res.text, xml_type)
        tbody = Soup.find('tbody')
        tdlist = tbody.find_all('td', attrs={'data-title': 'IP'})
        for td in tdlist:
            self.__ipList.append(td.get_text().strip())
        return self.__ipList


request = download()
