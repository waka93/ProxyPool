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

    def craw_hidemy(self):
        url = FREE_PROXY_URL2
        print('Getting proxies from ', url)
        headers = {
            'cookie': '__cfduid=dd2bd5386b3a230280c9fc019682498941526857889; _ga=GA1.2.760480060.1526857895; _gid=GA1.2.1401328965.1526857895; _ym_uid=1526857895705360794; PAPVisitorId=792e2357297ace321a57ecbcfdYI398j; PAPVisitorId=792e2357297ace321a57ecbcfdYI398j; jv_refer_EBSrukxUuA=https%3A%2F%2Fhidemy.name%2Fen%2Fproxy-list%2F; t=65879552; cf_clearance=54eeeafa2d1a76e9266f3d252f5891ce10884e0b-1526946702-86400; _dc_gtm_UA-90263203-1=1; _ym_isad=1; _ym_wasSynced=%7B%22time%22%3A1526946706213%2C%22params%22%3A%7B%22webvisor%22%3A%7B%22date%22%3A%222011-10-31%2016%3A20%3A50%22%7D%2C%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; jv_enter_ts_EBSrukxUuA=1526946709147; jv_visits_count_EBSrukxUuA=2; jv_utm_EBSrukxUuA=; _ym_visorc_42065329=w; jv_pages_count_EBSrukxUuA=8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pattern = re.compile('<td class=tdl>(.*?)</td><td>(.*?)</td>')
            for address, port in re.findall(pattern, response.text):
                proxy = address + ':' + port
                yield proxy
        if response.status_code == 503:
            print('Cookie needs to be updated')
            return None
        return None

    def craw_kuaidaili(self):
        url = FREE_PROXY_URL3
        print('Getting proxies from ', url)
        pages = range(1, 11)
        pattern = re.compile('.*?"IP">(.*?)</td>.*?"PORT">(.*?)</td>', re.S)
        for page in pages:
            new_url = url + str(page) + '/'
            response = requests.get(new_url, headers=HEADERS)
            if response.status_code == 200:
                for address, port in re.findall(pattern, response.text):
                    proxy = address + ':' + port
                    yield proxy
            continue
        return None


if __name__ == '__main__':
    pass
