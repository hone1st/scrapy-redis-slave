import re
import logging
from scrapy_redis.spiders import RedisSpider
from slave168.items import Slave168Item
from slave168.utils.redisutil import UtilRedis


class SlaveSpider(RedisSpider):

    # name = slave186
    name = 'slave1862'
    redis_key = 'detailurl:'

    def parse(self, response):
        redis = UtilRedis()
        item = Slave168Item()
        all_msg = response.css('div.ptlxfsC>ul>li')[0]
        try:
            # 姓名一般为2-3个所以
            item['name'] = all_msg.re('[\u4e00-\u9fa5]{2,3}')[0]
            # 电话
            if all_msg.re('\d+[-\s]+\d+'):
                item['telphone'] = all_msg.re('\d+[-\s]+\d+')[0]
            else:
                item['telphone'] = '0759-7174717'
            # 手机
            if all_msg.re('\d{11}'):
                item['phone'] = all_msg.re('\d{11}')[0]
            else:
                item['phone'] = '11111111111'
            # 地址
            address = re.findall('[\u4e00-\u9fa5]+[0-9a-zA-Z]?[\u4e00-\u9fa5]?', all_msg.re('地址.*</p>')[0])
            address = [i for i in address if i[-3:] != '产品网']
            item['address'] = ''.join(address)[2:]
            # 网址
            item['host'] = all_msg.re('h.*m/<')[0][:-1]
            # QQ 如果存在
            if all_msg.re('QQ：\d+'):
                item['qq'] = all_msg.re('QQ：\d+')[0][3:]
            else:
                item['qq'] = '123456'
            # print(item)
            item['url'] = response.url

        except:
            redis.conn.sadd('indexExcepturls:', response.url)
            logging.debug(msg='已将索引异常的数据的url：' + response.url + '存储到indexExcepturls:中了')
            return None
        else:
            yield item