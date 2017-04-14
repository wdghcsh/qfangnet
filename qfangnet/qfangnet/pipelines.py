# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import logging
logger = logging.getLogger(__name__)

class QfangnetPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.collection = self.connection.settings['MONGODB_DB'].settings['MONGODB_COLLECTION']


    def process_item(self, item, spider):
        valid = True
        catory = item["catory"] if item["catory"] else settings['MONGODB_DB']
        city = item["city"] if item["city"] else settings['MONGODB_COLLECTION']
        collection = self.connection[catory]
        collection = collection[city]
        if not collection.find_one({"link": item['link']}):
            for data in item:
                if not data:
                    valid = False
                    raise DropItem("Missing {0}!".format(data))
            if valid:
                try:
                    collection.insert(dict(item))
                    logging.info("Data success added to city database!")
                except:
                    self.collection.insert(dict(item))
                    logging.info("Data success added to unknow database!")
        else:
            logging.info('%s' % item)
            logging.info('%s already exists in datebase.' % item['link'])
        return item


class LianjiaPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.collection = self.connection.Lianjia['Lianjia0414']


    def process_item(self, item, spider):
        valid = True
        if item['ljlink']:
            catory = item["catory"] if item["catory"] else 'Lianjia'
            city = item["city"] if item["city"] else 'Lianjia0414'
            collection = self.connection[catory[city]]
            if not collection.find_one({"ljlink": item['ljlink']}):
                for data in item:
                    if not data:
                        valid = False
                        raise DropItem("Missing {0}!".format(data))
                if valid:
                    try:
                        collection.insert(dict(item))
                        logging.info("Data success added to city database!")
                    except:
                        self.collection.insert(dict(item))
                        logging.info("Data success added to unknow database!")
            else:
                logging.info('%s' % item)
                logging.info('%s already exists in datebase.' % item['ljlink'])
            return item
        else:
            return item