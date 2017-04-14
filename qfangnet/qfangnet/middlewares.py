# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import os
import logging
from datetime import datetime, timedelta
from twisted.web._newclient import ResponseNeverReceived
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError
import heapq
import fetch_free_proxy


logger = logging.getLogger(__name__)

class RandomUserAgent(object):
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class QfangnetSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HttpProxyMiddleware(object):

    def __init__(self, settings):
        """proxy = address:port"""
        self.proxies = [{'proxy': None, 'rate': 1.0, 'count': 888, 'fail': 0}]
        self.proxy_file = "proxies.txt"
        self.last_time_fetch_proxy = datetime.now()
        """ 前N个高成功率的Proxy"""
        self.top_proxy_num = 5
        """强制获取新代理的时间(min)"""
        self.fetch_proxy_interval = 120
        self.last_proxy_index = None
        if os.path.exists(self.proxy_file):
            with open(self.proxy_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line and self.isexistproxy(line):
                        self.proxies.append({'proxy': line, 'rate': 1.0, 'count': 0, 'fail': 0})
        self.proxies.remove({'proxy': None, 'rate': 1.0, 'count': 888, 'fail': 0})

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def fetch_proxy(self):
        new_proxies = fetch_free_proxy.main()
        with open(self.proxy_file, 'a') as fw:
            for each in new_proxies:
                if each and self.isexistproxy(each):
                    self.proxies.append({'proxy': each, 'rate': 1.0, 'count': 0, 'fail': 0})
                    fw.write(each + '\n')
        self.last_time_fetch_proxy = datetime.now()

    def isexistproxy(self, proxy):
        for each in self.proxies:
            if proxy != each['proxy']:
                return True

    def check_proxy_status(self, request):
        if len(self.proxies) < 10:
            logging.info('Proxies < 10, Staring fetct new proxies')
            self.fetch_proxy()
        self.top_rate_proxy = heapq.nlargest(self.top_proxy_num, self.proxies, key=lambda x: x['rate'])
        average_rate = sum([x['rate'] for x in self.top_rate_proxy]) / float(self.top_proxy_num)
        if average_rate < 0.5:
            logging.info('%s' % self.top_rate_proxy)
            logging.info('The average_rate(%s) < 0.5, Staring fetct new proxies' % average_rate)
            self.fetch_proxy()
        if datetime.now() > self.last_time_fetch_proxy + timedelta(minutes=self.fetch_proxy_interval):
            logging.info('last time along , Staring fetct new proxies')
            self.fetch_proxy()

    def check_request(self, request):
        fail_proxy_index = request.meta['proxy_index']
        self.proxies[fail_proxy_index]['fail'] = self.proxies[fail_proxy_index]['fail'] + 1
        if self.proxies[fail_proxy_index]['count'] > 5:
            self.proxies[fail_proxy_index]['rate'] = 1 - float(self.proxies[fail_proxy_index]['fail']) / float(self.proxies[fail_proxy_index]['count'])

    def set_request(self, request):
        self.top_rate_proxy = heapq.nlargest(self.top_proxy_num, self.proxies, key=lambda x: x['rate'])
        proxy_group = random.choice(self.top_rate_proxy)
        proxy = proxy_group['proxy'].strip('\n')
        request.meta["proxy"] = 'http://' + proxy
        proxy_index = self.proxies.index(proxy_group)
        request.meta['proxy_index'] = self.proxies.index(proxy_group)
        self.proxies[proxy_index]['count'] = self.proxies[proxy_index]['count'] + 1

    def process_request(self, request, spider):
        """ 将request设置为使用代理"""
        self.check_proxy_status(request)
        if "Fail_proxy" in request.meta.keys() and request.meta['Fail_proxy']:
            self.check_request(request)
        self.set_request(request)

    def process_response(self, request, response, spider):
        """根据response的status.code，借此判断是否更换代理"""
        if response.status != 200:
            request.meta['Fail_proxy'] = True
            new_request = request
            return new_request
        else:
            return response

    def process_exception(self, request, exception, spider):
        DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)
        if isinstance(exception, DONT_RETRY_ERRORS):
            request.meta['Fail_proxy'] = True
            new_request = request
            return new_request