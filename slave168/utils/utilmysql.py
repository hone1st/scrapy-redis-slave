import pymysql
from DBUtils.PooledDB import PooledDB


class UtilMysql(object):
    __instance = None
    __flag = True

    def __new__(cls, *args, **kwargs):
        # 如果None  创建对象
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    # """
    #     @sql: 该sql是用来查询表的存在是否的sql语句
    #     @table_name：该table_name和sql是共同存在的
    #     @creat_sql: 该sql是创建表的操作的sql
    # """

    def __init__(self, sql=None, table_name=None, create_sql=None):
        if self.__flag:
            self.pool = self.__init__mysql(sql, table_name, create_sql)
            self.__flag = False

    def __init__mysql(self, sql, table_name, create_sql):
        host = '127.0.0.1'
        user = 'root'
        passwd = 'root'
        mincached = 10
        creator = pymysql
        db = 'testpool'
        port = 3306

        pool = PooledDB(creator=creator, db=db, port=port, mincached=mincached,
    host=host, user=user, passwd=passwd)
        #
        # '''
        #     # 判断表是否存在
        #     sql = SELECT table_name FROM information_schema.TABLES WHERE table_name ='%s' % table_name
        # '''
        # if sql is not None and table_name is not None:
        #     conn = pool.connection()
        #     cur = conn.cursor()
        #     res = cur.execute(sql)
        #     if res == 1:
        #         print('！表已存在')
        #     elif sqls is []:
        #         print('不执行增删查改操作')


        return  pool

if __name__ == '__main__':
    a = UtilMysql()
