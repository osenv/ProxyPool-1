from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
import base64

BASE_URL = 'http://free-proxy.cz/en/proxylist/country/all/http/ping/all/{page}'
MAX_PAGE = 5


class CzFreeProxyCrawler(BaseCrawler):
    """
    free-proxy.cz crawler, http://free-proxy.cz/en/proxylist/country/all/http/ping/all/1
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        trs = doc('#proxy_list > tbody > tr').items()
        for tr in trs:
            try:
                _host = tr.find('td:nth-child(1) > script').text().replace('document.write(Base64.decode("', '').replace('"))', '')
                host = base64.b64decode(_host.encode('utf-8')).decode('utf-8')
                port = int(tr.find('td:nth-child(2) > span').text())
                yield Proxy(host=host, port=port)
            except:
                continue


if __name__ == '__main__':
    crawler = CzFreeProxyCrawler()
    for proxy in crawler.crawl():
        print(proxy)
