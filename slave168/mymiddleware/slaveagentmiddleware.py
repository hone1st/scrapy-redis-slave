import random
import logging

from scrapy.exceptions import IgnoreRequest

# 导入redis的connect开门钥匙
from slave168.settings import AGENT_POOL
from slave168.utils.redisutil import UtilRedis

# 导入TRYTIME和AGENTPOOL在setting.py中


class SlaveAgentMiddleware(object):

    # process_request(self, request, spider)

    def process_request(self, request, spider):
        # 第一次初始化UtilRedis
        conn = UtilRedis().conn
        # 随机设置请求头
        request.headers["User-Agent"] = random.choice(AGENT_POOL)
        # 判断trytime的次数来决定在失败后是否执行其他中间件的process_request还是reise掉
        # or r.sismember('hadgetdetailurl:', request.url) == 1 只有在salve中添加
        if conn.sismember('completeurl:', request.url) or conn.sismember('indexExcepturls:', request.url):
            logging.debug(msg=request.url + ':该url已将爬取过了！')
            # 记录被忽略掉的url   master中不记录被忽略掉的url
            raise IgnoreRequest("IgnoreRequest: %s" % request.url)
