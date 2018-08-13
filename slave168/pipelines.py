# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from slave168.utils.utilmysql import UtilMysql
from slave168.utils.redisutil import UtilRedis

import logging


class Slave168Pipeline(object):

    def process_item(self, item, spider):
        redis = UtilRedis()
        mysql = UtilMysql()
        conn = mysql.pool.connection()
        cur = conn.cursor()
        # name/telphone/phone/address/host/qq
        sql = "INSERT INTO pool(name, telphone, phone, address, host, qq) VALUES " \
              "('%s', '%s', '%s', '%s', '%s', '%s')" % \
              (item['name'], item['telphone'], item['phone'], item['address'], item['host'], item['qq'])
        try:
            cur.execute(sql)
            conn.commit()
            redis.conn.sadd('completeurl:', item['url'])
            logging.info(msg='成功存储了url：' + item['url'] + '的数据')
        except:
            cur.rollback()
        conn.close()


# if __name__ == '__main__':
#     item = {
#         'name': '1',
#         'telphone': '2',
#         'phone': '3',
#         'address': '4',
#         'host': '5',
#         'qq': '6'
#     }
#     a = Slave168Pipeline()
#     a.process_item(item)
