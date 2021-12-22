import os
import logging
import logging.config

from cfg import Config


LOG_BASE_DIR = Config.APP_LOG_PATH
APP_NAME = Config.APP_NAME

LOG_APP_NAME = Config.LOG_APP_NAME
LOG_DB_NAME = Config.LOG_DB_NAME
LOG_ER_NAME = Config.LOG_ER_NAME
LOGGER_LEVEL = Config.LOGGER_LEVEL

app_log_path = os.path.join(LOG_BASE_DIR, APP_NAME)
if not os.path.exists(app_log_path):
    os.makedirs(app_log_path)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s][%(asctime)s][%(process)d][%(threadName)s:%(thread)d][%(filename)s:%(lineno)d][%(funcName)s][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'collect': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        # 终端日志
        'console': {
            'level': LOGGER_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 应用文件日志，收集info及以上的日志
        'default': {
            'level': LOGGER_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(app_log_path, LOG_APP_NAME),  # 日志文件
            'when': 'D',
            'backupCount': 100,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 应用文件日志，收集错误及以上的日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(app_log_path, LOG_ER_NAME),  # 日志文件
            'maxBytes': 1024 * 1024 * 500,  # 日志大小 5M
            'backupCount': 100,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 数据库层日志
        'db': {
            'level': LOGGER_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(app_log_path, LOG_DB_NAME),
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': "utf-8"
        }
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console', 'error'],
            'level': LOGGER_LEVEL,
            'propagate': True,
        },
        # logging.getLogger('db')拿到的logger配置
        'db': {
            'handlers': ['db'],
            'level': LOGGER_LEVEL,
        },
    },
}


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
db_logger = logging.getLogger("db")


if __name__ == '__main__':
    logger.info('应用日志。。。')
    logger.error('应用出错日志。。。')
    db_logger.error('数据库访问日志')
    logger.debug('debug --- ')
