import pymysql
from DBUtils.PooledDB import PooledDB


class UtilMysql(object):

    @classmethod
    def getconn(self):
        pool = PooledDB(pymysql, 5, host='127.0.0.1', user='root', passwd='root', db='testpool', port=3306)
        return pool.connection()

if __name__ == '__main__':
    pass