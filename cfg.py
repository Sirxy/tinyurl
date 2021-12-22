"""
配置参数
"""
import os


class Config(object):
    # 日志
    LOGGER_LEVEL = "INFO"  # 日志级别
    APP_LOG_PATH = r"D:\app\logs"  # 日志存储目录
    LOG_APP_NAME = "shorturl.log"  # INFO日志
    LOG_ER_NAME = "shorturl_error.log"  # Error日志
    LOG_DB_NAME = 'shorturl_db.log'

    # 应用名称
    APP_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    APP_NAME = APP_BASE_DIR.split(os.sep)[-1]

    # IP和端口
    APP_HOST = "127.0.0.1"
    APP_PORT = "5010"

    # 数据库
    HOST = '127.0.0.1'
    PORT = 3306
    USER = 'root'
    PASSWORD = '123456'
    DB = 'tinyurl'
    CHARSET = 'utf8'
