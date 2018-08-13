# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Slave168Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
        目前爬取字段为：
            名字、电话、手机、地址、网站、QQ
            name/telphone/phone/address/host/qq
    """
    name = scrapy.Field()
    telphone = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()
    host = scrapy.Field()
    qq = scrapy.Field()
    url = scrapy.Field()