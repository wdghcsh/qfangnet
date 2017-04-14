#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
from lxml import etree
import threading
import Queue
import logging
logger = logging.getLogger(__name__)
q = Queue.Queue()


class MyThread(threading.Thread):
    """重写threading.Thread"""
    def __init__(self, target=None, kwargs=None):
        threading.Thread.__init__(self, target=None)
        self.kwargs = kwargs
        self.target = target

    def run(self):
        q.put(self.target(self.kwargs))


def get_selector(url, timeout=5):
    tryNum = 1
    while tryNum <= 10:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/45.0.2454.99 Safari/537.36"}
            request = urllib2.Request(url, headers=headers)
            html = urllib2.urlopen(request, timeout=timeout).read()
            selector = etree.HTML(html)
            return selector
        except Exception:
            tryNum += 1
            continue


def get_proxyA():
    urls = ['http://www.xsdaili.com/mfdl?type=1',
            'http://www.kxdaili.com/dailiip.html',
            'http://www.ip181.com/',
            'http://www.nianshao.me/?stype=1',
            'http://www.yun-daili.com/',
            'http://www.bigdaili.com/dailiip.html',
            'http://img.kuaidaili.com/free/',
            'http://www.nianshao.me/?stype=2',
            'http://httpsdaili.com/free.asp?stype=1',
            ]
    proxyA_proxies = []
    for each in urls:
        logger.debug("Start Crawling %s" % each)
        try:
            ips = get_selector(each).findall('.//tr')
        except:
            continue
        for i in range(1, len(ips)):
            try:
                ip_temp = ips[i].xpath('./td[1]/text()')[0] + ':' + ips[i].xpath('./td[2]/text()')[0]
                ip_temp = ip_temp.strip()
                proxyA_proxies.append(ip_temp)
            except:
                continue
    return proxyA_proxies


def get_proxyB():
    urls = [
        'http://www.dlip.cn/gng/',
            'http://www.dlip.cn/gwg/',
            'http://www.xicidaili.com/nn/',
            ]
    proxyB_proxies = []
    for each in urls:
        logger.debug("Start Crawling %s" % each)
        try:
            ips = get_selector(each).findall('.//tr')
        except:
            continue
        for i in range(1, len(ips)):
            try:
                ip_temp = ips[i].xpath('./td[2]/text()')[0] + ':' + ips[i].xpath('./td[3]/text()')[0]
                ip_temp = ip_temp.strip() + '\n'
                proxyB_proxies.append(ip_temp)
            except:
                continue
    return proxyB_proxies


def check_proxies(proxy, check_times=5, timeout=5):
    url = "http://ip.chinaz.com/getip.aspx"
    while check_times > 0:
        proxy_handler = urllib2.ProxyHandler({'http': 'http://' + proxy.strip('\n')})
        opener = urllib2.build_opener(proxy_handler)
        try:
            html = opener.open(url, timeout=timeout).read()
            if '61.141' not in html:
                return proxy.strip('\n')
            else:
                return False
        except Exception:
            check_times -= 1
            continue
    else:
        return False


def main():
    proxies = []
    validproxies = []
    proxies += get_proxyA()
    proxies += get_proxyB()
    logger.debug("Finished Crawling Proxy, Now Checking Proxies.")
    proxies = set(proxies)
    for check_proxy in proxies:
        # proxy_host = {'http': 'http://' + check_proxy.strip('\n')}
        t = MyThread(target=check_proxies, kwargs=check_proxy)
        t.start()
    while True:
        try:
            ip = q.get(timeout=5)
            if ip:
                validproxies.append(ip)
        except Queue.Empty:
            logger.debug("Finished Fetch Proxies" )
            break
    return list(set(validproxies))

if __name__ == "__main__":
    for each in main():
        print each
