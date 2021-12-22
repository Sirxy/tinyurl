import pymysql
import time
from functools import wraps
from DBUtils.PooledDB import PooledDB, SharedDBConnection
from util.log import logger


def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


def execute_time(func):

    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        start_local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = func(*args, **kwargs)
        end = time.time()
        end_local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print("print:", end - start)
        log = "Function: %s, start: @%s, end: @%s,  elapsed: @%.4fs." % (func.__name__, start_local, end_local, end - start)
        # print("printlog:", log)
        logger.info(log)
        return result
    return inner


@singleton
class MySQL(object):
    # 操作MySQL数据库

    __pool = None  # 连接池对象

    def __init__(self, config):
        """初始化连接池"""
        try:
            self.config = config
            # 数据库构造函数，从连接池中取出连接，并生成操作游标
            self.pool = self.__get_conn() 

        except pymysql.Error:
            raise

    def __get_conn(self):
        """
        从连接池中取出连接
        """
        host = self.config.get('HOST')
        port = self.config.get('PORT') if type(self.config.get('PORT'))== int else int(self.config.get('PORT'))
        user = self.config.get('USER')
        password = self.config.get('PASSWORD')
        database = self.config.get('DB')
        charset = self.config.get('CHARSET')

        if self.__pool is None:
            __pool = PooledDB(
                creator=pymysql,  # 使用链接数据库的模块
                maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
                mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
                maxshared=3,  # 允许的最大共享连接数（默认值为0或无表示所有连接都是专用的）当达到此最大数量时，连接将停止，如果它们被请求为可共享，则为共享。
                blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
                setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
                ping=0,  # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset=charset
            )
            MySQL.__pool = __pool

        return MySQL.__pool

    def get_cursor(self):
        """
        """
        try:
            conn = MySQL.__pool.connection()
            cursor = conn.cursor()

            return conn, cursor
        except Exception as e:
            raise e

    @execute_time
    def execute(self, sql):
        """
        执行一条SQL：insert、update、delete
        """
        try:

            conn, cursor = self.get_cursor()

            cursor.execute(sql)
            conn.commit()
            # affected_row = cursor.rowcount
            lastrowid = cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise str(e)
        finally:
            cursor.close()
            conn.close()

        # return affected_row
        return lastrowid

    @execute_time
    def query_one(self, sql):
        """
        执行SQL，查询一条记录：select
        """
        try:
            conn, cursor  = self.get_cursor()

            cursor.execute(sql)
            result = cursor.fetchone()
        
        except Exception as e:
            raise str(e)
        finally:
            cursor.close()
            conn.close()
        
        return result

    @execute_time
    def query_many(self, sql):
        """
        执行SQL，查询多条记录：select
        """

        pass


if __name__ == "__main__":

    pass
