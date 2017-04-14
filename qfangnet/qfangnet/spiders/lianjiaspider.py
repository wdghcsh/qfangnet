#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from qfangnet.items import QfangnetItem, LianjiaItem
import logging
logger = logging.getLogger(__name__)


class lianjiaspider(CrawlSpider):
    name = 'lianjia'
    allowed_domains = ["lianjia.com"]
    deny_domains = []
    start_urls = ["https://sz.lianjia.com/"]
    sale_item = "Sale"
    rent_item = "Rent"
    cities = {'bj.lianjia.com': u'\u5317\u4eac', 'cd.lianjia.com': u'\u6210\u90fd', 'cq.lianjia.com': u'\u91cd\u5e86',
              'cs.lianjia.com': u'\u957f\u6c99', 'dl.lianjia.com': u'\u5927\u8fde', 'dg.lianjia.com': u'\u4e1c\u839e',
              'fs.lianjia.com': u'\u4f5b\u5c71', 'gz.lianjia.com': u'\u5e7f\u5dde', 'hz.lianjia.com': u'\u676d\u5dde',
              'hk.lianjia.com': u'\u6d77\u53e3', 'hf.lianjia.com': u'\u5408\u80a5', 'jn.lianjia.com': u'\u6d4e\u5357',
              'ls.lianjia.com': u'\u9675\u6c34', 'nj.lianjia.com': u'\u5357\u4eac', 'qd.lianjia.com': u'\u9752\u5c9b',
              'qh.lianjia.com': u'\u743c\u6d77', 'sh.lianjia.com': u'\u4e0a\u6d77', 'sz.lianjia.com': u'\u6df1\u5733',
              'su.lianjia.com': u'\u82cf\u5dde', 'sjz.lianjia.com': u'\u77f3\u5bb6\u5e84', 'sy.lianjia.com': u'\u6c88\u9633',
              'san.lianjia.com': u'\u4e09\u4e9a', 'tj.lianjia.com': u'\u5929\u6d25', 'wh.lianjia.com': u'\u6b66\u6c49',
              'wc.lianjia.com': u'\u6587\u660c', 'wn.lianjia.com': u'\u4e07\u5b81', 'xm.lianjia.com': u'\u53a6\u95e8',
              'xa.lianjia.com': u'\u897f\u5b89', 'yt.lianjia.com': u'\u70df\u53f0', 'zs.lianjia.com': u'\u4e2d\u5c71',
              'zh.lianjia.com': u'\u73e0\u6d77'}
    rules = [
        Rule(LinkExtractor(allow=('/pg\d\d?/|ershoufang/\d{8,16}.html|ershoufang/([a-zA-Z]){3,}\d?/|ershoufang/$'),
                           deny=('/([a-zA-z]{1,3}\d{1,2}){2,}/|/\d+/|/[a-z]\d/|%|/[^pg][^pg]\d\d?/')),
             follow=True, callback='parse_sale'),
        Rule(LinkExtractor(allow=('/pg\d\d?/|zufang/\d{8,16}.html|zufang/([a-zA-Z]){3,}\d?/|zufang/$'),
                           deny=('/([a-zA-z]{1,3}\d{1,2}){2,}/|/\d+/|/[a-z]\d/|%|/[^pg][^pg]\d\d?/')),
             follow=True, callback='parse_rent'),
    ]

    def parse_sale(self, response):
        item = LianjiaItem()
        selector = Selector(response)
        targets = selector.xpath('//*[@class="sellListContent"]/li')
        item['catory'] = self.sale_item
        try:
            item['city'] = self.cities[re.findall('([a-z]{2,3}\.lianjia\.com)', response.url)[0]]
        except:
            item['city'] = None
        for each in targets:
            item['ljlink'] = each.xpath('./a/@href').extract_first()
            item['image_link'] = each.xpath('./li/a/img/@src').extract_first()
            item['keyword'] = each.xpath('.//[@class="title"]/a/text()').extract_first()
            item['garden'] = each.xpath('.//[@class="houseInfo"]/a/text()').extract_first()
            item['informations'] = each.xpath('.//[@class="houseInfo"]/text()')[0].extract().split('|').strip()
            item['Info'] = each.xpath('.//[@class="positionInfo"]/text()').extract_first().replace('-', '').strip()
            item['metro'] = each.xpath('.//[@class="positionInfo"]/a/text()').extract_first()
            item['follower'] = each.xpath('.//[@class="followInfo"]/text()')[0].extract().split('/').strip()
            item['tags'] = each.xpath('.//[@class="tag"]/span/text()').extract()
            item['price'] = each.xpath('.//[@class="totalPrice"]/span/text()').extract_first() + u'万'
            item['unitprice'] = each.xpath('.//[@class="unitPrice"]/span/text()').extract_first()
            yield item
        try:
            target = Selector(response).xpath('//*[@class="page-box house-lst-page-box"]/@page-data').extract_first()
            page_num = eval(target)['totalPage']
            for i in range(1, page_num + 1):
                if '/pg' in url:
                    result = re.sub('/pg\d+', '/pg%d/' % i, url)
                else:
                    result = url + 'pg%d' % i
                yield Request(url=result, callback=self.parse_sale)
        except:
            pass

    def parse_rent(self, response):
        item = LianjiaItem()
        selector = Selector(response)
        item['catory'] = self.rent_item
        try:
            item['city'] = self.cities[re.findall('([a-z]{2,3}\.lianjia\.com)', response.url)[0]]
        except:
            item['city'] = None
        targets = selector.xpath('//*[@class="house-lst"]/li')
        for each in targets:
            item['ljlink'] = each.xpath('.//[@class="pic-panel"]/a/@href').extract_first()
            item['image_link'] = each.xpath('.//[@class="pic-panel"]/a/img/@src').extract_first()
            item['keyword'] = each.xpath('.//[@class="info-panel"]/h2/a/text()').extract_first()
            item['garden'] = each.xpath('.//[@class="region"]/text()').extract_first()
            item['zone'] = each.xpath('.//[@class="zone"]/span/text()').extract_first()
            item['area'] = each.xpath('.//[@class="meters"]/text()').extract_first()
            item['oriention'] = each.xpath('.//[@class="where"]/span')[-1].extract()
            item['metro'] = each.xpath('.//[@class="con"]/a/text()').extract_first().replace(u'租房', '')
            item['floor'] = each.xpath('.//[@class="con"]/text()').extract()
            item['subway'] = each.xpath('.//[class="fang-subway-ex"]/span/text()').extract_first()
            item['visit'] = each.xpath('.//[@class="haskey-ex"]/span/text()').extract_first()
            item['decoration'] = each.xpath('.//[@class="decoration-ex"]/span/text()').extract_first()
            item['num'] = each.xpath('.//[@class="num"]/text()').extract_first()
            item['update'] = each.xpath('.//[@class="price-pre"]/text()').extract_first()
            item['count'] = each.xpath('.//[@class="square"]/div/span/text()').extract_first()
            yield item
        try:
            target = Selector(response).xpath('//*[@class="page-box house-lst-page-box"]/@page-data').extract_first()
            page_num = eval(target)['totalPage']
            for i in range(1, page_num + 1):
                if '/pg' in url:
                    result = re.sub('/pg\d+', '/pg%d/' % i, url)
                else:
                    result = url + 'pg%d' % i
                yield Request(url=result, callback=self.parse_rent)
        except:
            pass