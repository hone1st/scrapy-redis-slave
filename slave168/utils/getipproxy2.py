import telnetlib
import requests
import re
import logging
import threading

# from slave168.settings import IP_PROXY_TIME_OUT
# 改变为单例模式,无论创建多少个对象都是初始化一次


class GetIpProxyUtil(object):
    __species = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self):
        if self.__first_init:
            self.proxys = []
            self.__initproxiesip()
            self.__class__.__first_init = False

    def __getproxiesip(self):
        proxys = []
        headers = {
            'Host': 'www.66ip.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.66ip.cn/nm.html',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        complie = '\d+\.\d+\.\d+\.\d+:\d+'
        # 测试300个代理ip
        url = 'http://www.66ip.cn/nmtq.php?getnum=300&isp=0&anonymoustype=3&start=&' \
              'ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip'
        content = requests.get(url=url, headers=headers)
        ip_ports = re.findall(complie, content.text)
        for ip_port in ip_ports:
            proxys.append({'ip': ip_port.split(':')[0],
                           'port': ip_port.split(':')[-1]})
        return proxys

# telnet测试

    def __initproxiesip(self):
        proxys = self.__getproxiesip()
        proxy_thread = []
        for proxy in proxys:
            t = threading.Thread(target=self.__testip, args=(proxy, ))
            t.setDaemon(True)
            proxy_thread.append(t)
        for t in proxy_thread:
            t.start()
        for t in proxy_thread:
            t.join()

    def __testip(self, proxy):
        try:
            # 测试连接时间为0.5秒
            telnetlib.Telnet(proxy['ip'], port=proxy['port'], timeout=0.5)
        except Exception as e:
            logging.log(logging.ERROR, msg=proxy['ip'] + ":" + proxy['port'] + "该代理ip不可用，测试超时")
        else:
            print(proxy['ip'] + ":" + proxy['port'] + "该代理ip可用，测试成功，正在存储ing")
            self.proxys.append(proxy['ip'] + ":" + proxy['port'])


if __name__ == '__main__':
    a = GetIpProxyUtil()
    print(a.proxys)
    #
    # b = GetIpProxyUtil()
    # print(b.proxys)