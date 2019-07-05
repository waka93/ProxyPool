import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import re
from bin.config import *


def get_html(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('Cannot connect to ', url)
        return None


class ProxiesGetterMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['_func'] = []
        for k, v in attrs.items():
            if 'craw_' in k:
                attrs['_func'].append(k)
                count += 1
        attrs['_count'] = count
        return type.__new__(cls, name, bases, attrs)


class ProxiesGetter(object, metaclass=ProxiesGetterMetaclass):
    def get_proxies(self, craw_func):
        proxies = []
        for proxy in eval('self.{}()'.format(craw_func)):
            proxies.append(proxy)
        return proxies

    def craw_free_proxy_list(self):
        url = FREE_PROXY_URL1
        print('Getting proxies from ', url)
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            table = soup.select('tbody')
            for row in table[0].select('tr'):
                address, port = [td.text for td in row.select('td')][0:2]
                proxy = address + ':' + port
                yield proxy
        return None

    # def craw_hidemy(self):
    #     url = FREE_PROXY_URL2
    #     print('Getting proxies from ', url)
    #     headers = {
    #         'cookie': FREE_PROXY_URL2_COOKIES,
    #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    #     }
    #     response = requests.get(url, headers=headers)
    #     if response.status_code == 200:
    #         pattern = re.compile('<td class=tdl>(.*?)</td><td>(.*?)</td>')
    #         for address, port in re.findall(pattern, response.text):
    #             proxy = address + ':' + port
    #             yield proxy
    #     if response.status_code == 503:
    #         print('Cookie needs to be updated')
    #         return None
    #     return None

    # def craw_kuaidaili(self):
    #     url = FREE_PROXY_URL3
    #     print('Getting proxies from ', url)
    #     pages = range(1, 11)
    #     pattern = re.compile('.*?"IP">(.*?)</td>.*?"PORT">(.*?)</td>', re.S)
    #     for page in pages:
    #         new_url = url + str(page) + '/'
    #         response = requests.get(new_url, headers=HEADERS)
    #         if response.status_code == 200:
    #             for address, port in re.findall(pattern, response.text):
    #                 proxy = address + ':' + port
    #                 yield proxy
    #         continue
    #     return None


if __name__ == '__main__':
    pass
