import redis


class UtilRedis(object):
    __species = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self):
        if self.__first_init:
            self.conn = self.__class__.__getrdeisconnect()
            self.__class__.__first_init = False

    @classmethod
    def __getrdeisconnect(cls):
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        return redis.Redis(connection_pool=pool)


if __name__ == '__main__':
    a = UtilRedis()
    a.redisconnect.sadd('111', 11)
    b = UtilRedis()
    b.redisconnect.sadd('2222', 22)