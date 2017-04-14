# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class QfangnetItem(Item):
    city = Field()
    catory = Field()
    image_link = Field()
    price = Field()
    area = Field()
    title = Field()
    link = Field()
    traffic_information = Field()
    keyword = Field()
    detail_layout = Field()
    detail_area = Field()
    detail_decoration = Field()
    detail_floor = Field()
    detail_year = Field()
    address_district = Field()
    address_metro = Field()
    address_road = Field()
    imgae_link = Field()
    floor = Field()
    completed_year = Field()
    subway_distance = Field()
    garden = Field()
    location = Field()
    tags = Field()
    total_price = Field()
    average_price = Field()


class LianjiaItem():
    ljlink = Field()
    image_link = Field()
    keyword = Field()
    garden = Field()
    zone = Field()
    area = Field()
    oriention = Field()
    metro = Field()
    floor = Field()
    subway = Field()
    visit = Field()
    decoration = Field()
    num = Field()
    update = Field()
    count = Field()
    informations = Field()
    Info  = Field()
    follower = Field()
    tags = Field()
    price = Field()
    unitprice = Field()
    city = Field()
    catory = Field()
# class OfficeItem(Item):
#     imgae_link = Field()
#     link = Field()
#     keyword = Field()
#     floor = Field()
#     city = Field()
#     catory = Field()
#     completed_year = Field()
#     subway_distance = Field()
#     garden = Field()
#     location = Field()
#     tags = Field()
#     area = Field()
#     total_price = Field()
#     average_price = Field()

