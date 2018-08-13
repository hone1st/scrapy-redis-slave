

from slave168.utils.redisutil import UtilRedis
from slave168.utils.getipproxy import GetIpProxyUtil

class SlaveIpProxyMiddleware(object):

    # process_response(self,request,response,spider)
    def process_response(self, request, response, spider):
        """
        :param request:
        :param response:
        :param spider:
        :return:

        起稿：初始化获取代理ip，随后根据请求的http和https不同，更换对应的代理ip。
        随后在判断重试次数和状态码来置换和删掉代理ip池中的超时ip
        """
        # 第一次初始化GetIpProxyUtil
        # 获取之前初始化过的UtilRedis对象
        proxys = GetIpProxyUtil().proxys
        conn = UtilRedis.conn
        # 获取response的状态码
        status = response.status
        if status//200 == 2:
            conn.sadd('completeurl:', response.url)
        return response
