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


class qfangnetspider(CrawlSpider):
    name = 'qfangnet'
    allowed_domains = ["qfang.com"]
    deny_domains = ["hk.qfang.com",
                    "hw.qfang.com",
                    "m.qfang.com",
                    "h5.qfang.com",
                    "baike.qfang.com",
                    "app.qfang.com",]
    start_urls = ["http://shenzhen.qfang.com"]
    pattern = re.compile('\.qfang\.com/rent.*')
    ex_pattern = '.qfang.com'
    sale_item = "Sale"
    rent_item = "Rent"
    offices_item = "OfficeSale"
    officer_item = "OfficeRent"
    rules = [
        Rule(LinkExtractor(allow=('com/sale/|qfang.com$|/f\d/|/f\d'), deny=(
            '[abcdghiklmoprtuy]\d{1,2}-+[a-z]\d{1,2}/?|/n0/?|hw.qfang.com|m.qfang.com|hk.qfang.com|/garden|(rent|sale)/\d+|/newhouse/?')),
             follow=True,
             callback='parse_sale'),
        Rule(LinkExtractor(allow=('com/rent/|qfang.com$|/f\d/|/f\d'), deny=(
            '[abcdghiklmoprtuy]\d{1,2}-+[a-z]\d{1,2}/?|/n0/?|hw.qfang.com|m.qfang.com|hk.qfang.com|/garden|(rent|sale)/\d+|/newhouse/?')),
             follow=True,
             callback='parse_rent'),
        Rule(LinkExtractor(allow=('com/office/rent/|qfang.com$|/n\d/|/n\d'), deny=(
            '[abcdghiklmoprtuy]\d{1,2}-+[a-z]\d{1,2}/?|/n0/?|hw.qfang.com|m.qfang.com|hk.qfang.com|/garden|(rent|sale)/\d+|/newhouse/?')),
             follow=True,
             callback='parse_office_rent'),
        Rule(LinkExtractor(allow=('com/office/sale/[a-z]+|qfang.com$|/n\d/|/n\d'), deny=(
            '[abcdghiklmoprtuy]\d{1,2}-+[a-z]\d{1,2}/?|/n0/?|hw.qfang.com|m.qfang.com|hk.qfang.com|/garden|(rent|sale)/\d+|/newhouse/?')),
             follow=True,
             callback='parse_office_sale')]

    def parse_sale(self, response):
        item = QfangnetItem()
        selector = Selector(response).xpath('//*[@id="cycleListings"]/ul/li')
        item['city'] = Selector(response).xpath('//*[@id="citySelected"]/span/text()').extract_first()
        item['catory'] = self.sale_item
        for each in selector:
            house_image_link = each.xpath('./a/img/@src').extract_first()
            item["image_link"] = re.sub('\.jpg.*', '.jpg', house_image_link).replace('\t', '').replace('\n', '').replace(
                '\r', '')
            item['price'] = each.xpath('//span[@class="sale-price"]/text()').extract_first() + u'万'
            item['area'] = each.xpath('//div[@class="show-price"]/p/text()').extract_first()
            item["title"] = each.xpath('./div[1]/p[3]/span[1]/a/text()').extract_first()
            item["link"] = re.sub(self.pattern, self.ex_pattern, response.url) + each.xpath(
                './div[1]/p[1]/a/@href').extract_first().replace(r'?insource=rent_list', '')
            item["traffic_information"] = each.xpath('./div[1]/p[5]/span/text()').extract()
            item['keyword'] = each.xpath('./div[1]/p[1]/a/text()').extract_first()
            item['detail_layout'] = each.xpath('./div[1]/p[2]/span[1]/text()').extract_first()
            item['detail_area'] = each.xpath('./div[1]/p[2]/span[3]/text()').extract_first()
            item['detail_decoration'] = each.xpath('./div[1]/p[2]/span[5]/text()').extract_first()
            item['detail_floor'] = ''.join(x.replace('\t', '').replace(' ', '') for x in
                                           each.xpath('./div[1]/p[2]/span[7]/text()').extract_first().splitlines())
            item['detail_year'] = each.xpath('./div[1]/p[2]/span[9]/text()').extract_first()
            item['address_district'] = each.xpath('./div[1]/p[3]/span[2]/a[1]/text()').extract_first()
            item['address_metro'] = ''.join(x.replace('\t', '').replace(' ', '') for x in
                                            each.xpath('./div[1]/p[3]/span[2]/a[2]/text()').extract_first().splitlines())
            item['address_road'] = each.xpath('./div[1]/p[3]/span[3]/text()').extract_first()
            yield item

    def parse_rent(self, response):
        item = QfangnetItem()
        selector = Selector(response).xpath('//*[@id="cycleListings"]/ul/li')
        item['city'] = Selector(response).xpath('//*[@id="citySelected"]/span/text()').extract_first()
        item['catory'] = self.rent_item
        for each in selector:
            house_image_link = each.xpath('./a/img/@src').extract_first()
            item["image_link"] = re.sub('\.jpg.*', '.jpg', house_image_link).replace('\t', '').replace('\n', '').replace('\r', '')
            item['price'] = each.xpath('//span[@class="sale-price"]/text()').extract_first() + u'元/月'
            item['area'] = each.xpath('//div[@class="show-price"]/p/text()').extract_first()
            item["title"] = each.xpath('./div[1]/p[3]/span[1]/a/text()').extract_first()
            item["link"] = re.sub(self.pattern, self.ex_pattern, response.url) + each.xpath('./div[1]/p[1]/a/@href').extract_first().replace(r'?insource=rent_list', '')
            item["traffic_information"] = each.xpath('./div[1]/p[5]/span/text()').extract()
            item['keyword'] = each.xpath('./div[1]/p[1]/a/text()').extract_first()
            item['detail_layout'] = each.xpath('./div[1]/p[2]/span[1]/text()').extract_first()
            item['detail_area'] = each.xpath('./div[1]/p[2]/span[3]/text()').extract_first()
            item['detail_decoration'] = each.xpath('./div[1]/p[2]/span[5]/text()').extract_first()
            item['detail_floor'] = ''.join(x.replace('\t', '').replace(' ', '') for x in each.xpath('./div[1]/p[2]/span[7]/text()').extract_first().splitlines())
            item['detail_year'] = each.xpath('./div[1]/p[2]/span[9]/text()').extract_first()
            item['address_district'] = each.xpath('./div[1]/p[3]/span[2]/a[1]/text()').extract_first()
            item['address_metro'] = ''.join(x.replace('\t', '').replace(' ', '') for x in each.xpath('./div[1]/p[3]/span[2]/a[2]/text()').extract_first().splitlines())
            item['address_road'] = each.xpath('./div[1]/p[3]/span[3]/text()').extract_first()
            yield item

    def parse_office_sale(self, response):
        item = QfangnetItem()
        target = Selector(response).xpath('//*[@class="cycle-listings-item clearfix "]')
        item["catory"] = self.offices_item
        item['city'] = Selector(response).xpath('//*[@class="cur-city-name"]/text()').extract_first()
        for each in target:
            item['imgae_link'] = each.xpath('.//@lazyload').extract_first().replace('\n', '').replace('\t', '').strip()
            item['link'] = each.xpath('.//@href').extract_first()
            item['keyword'] = each.xpath('.//h3/a/text()').extract_first()
            item['floor'] = each.xpath('.//*[@class="listings-item-characteristics clearfix"]/span[1]/text()'
                            ).extract_first().replace('\n', '').replace('\t', '').strip()
            item['completed_year'] = each.xpath(
                './/*[@class="listings-item-characteristics clearfix"]/span[1]/text()').extract_first().replace('\n',
                                                                                                                '').replace(
                '\t', '').strip()
            item['garden'] = each.xpath('.//*[@class="address-text"]/a/text()').extract_first().replace('\n', '').replace(
                '\t', '').strip()
            item['location'] = ''.join(each.xpath('.//*[@class="address-text"]/text()').extract()).replace('\n',
                                                                                                           '').replace('\t',
                                                                                                                       '').strip()
            item['subway_distance'] = ''.join(
                each.xpath('.//*[@class="subway-distance fl"]//span/text()').extract()).replace('\n', '').replace('\t',
                                                                                                                  '').strip()
            item['tags'] = each.xpath('.//*[@class="house-tags house-tags-new fl"]/span/text()').extract()
            item['area'] = each.xpath('.//*[@class="acreage"]/text()').extract_first()
            item['total_price'] = each.xpath('.//*[@class="onaverage-price"]/text()').extract_first()
            item['average_price'] = each.xpath('.//*[@class="listings-item-price"]/span/text()').extract_first()
            yield item

    def parse_office_rent(self, response):
        item = QfangnetItem()
        target = Selector(response).xpath('//*[@class="cycle-listings-item clearfix "]')
        item["catory"] = self.officer_item
        item['city'] = Selector(response).xpath('//*[@class="cur-city-name"]/text()').extract_first()
        for each in target:
            item['imgae_link'] = each.xpath('.//@lazyload').extract_first().replace('\n', '').replace('\t', '').strip()
            item['link'] = each.xpath('.//@href').extract_first()
            item['keyword'] = each.xpath('.//h3/a/text()').extract_first()
            item['floor'] = each.xpath('.//*[@class="listings-item-characteristics clearfix"]/span[1]/text()').extract_first().replace('\n', '').replace('\t', '').strip()
            item['completed_year'] = each.xpath('.//*[@class="listings-item-characteristics clearfix"]/span[1]/text()').extract_first().replace('\n', '').replace('\t', '').strip()
            item['garden'] = each.xpath('.//*[@class="address-text"]/a/text()').extract_first().replace('\n', '').replace('\t', '').strip()
            item['location'] = ''.join(each.xpath('.//*[@class="address-text"]/text()').extract()).replace('\n', '').replace('\t', '').strip()
            item['subway_distance'] = ''.join(each.xpath('.//*[@class="subway-distance fl"]//span/text()').extract()).replace('\n', '').replace('\t', '').strip()
            item['tags'] = each.xpath('.//*[@class="house-tags house-tags-new fl"]/span/text()').extract()
            item['area'] = each.xpath('.//*[@class="acreage"]/text()').extract_first()
            item['total_price'] = each.xpath('.//*[@class="onaverage-price"]/text()').extract_first()
            item['average_price'] = each.xpath('.//*[@class="listings-item-price"]/span/text()').extract_first()
            yield item

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

