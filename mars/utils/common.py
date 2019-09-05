import logging
from logging.handlers import TimedRotatingFileHandler
from werkzeug.routing import BaseConverter
from fake_useragent import UserAgent
from flask import current_app


class RegexConverter(BaseConverter):
    """自定义过滤器"""
    def __init__(self, url_map, regex):
        super(RegexConverter, self).__init__(url_map)
        self.regex = regex


class SpidersToolBox(UserAgent):
    def __init__(self, file_name=None, level=logging.DEBUG, db="wcc", ):
        super(SpidersToolBox, self).__init__()
        self.file_name = file_name
        self.level = level
        self.logger = self.__sethandler()

        # 数据库连接设置
        self.__db_name = db
        self.conn = self.__set_dbconnection()

    def __new__(cls, *more):
        cls.logs_path = current_app.config.get("LOG_DIR")
        # cls.logger = cls.__sethandler()

        # if not os.path.exists(cls.logs_path):
        #     os.makedirs(cls.logs_path)

        return object.__new__(cls)

    def __get_log_name(self):
        """如果是被继承,自动获取子类的类名作为日志文件名/如果是被单独调用,需要传入自定义日志文件名"""
        # 被实例化调用
        if self.__class__.__name__ == SpidersToolBox.__name__:
            if self.file_name:
                assert type(self.file_name) is str, TypeError("文件名应为字符串类型")
                if self.file_name.endswith(".log"):
                    return self.file_name[:-4]
                return self.file_name
            return self.file_name

        # 被继承的时候
        return self.__class__.__name__

    def __get_log_path(self):
        log_name = self.__get_log_name()
        if not log_name:
            return None
        path = self.logs_path / (log_name + ".log")
        return path

    def __sethandler(self):
        """配置日志handler"""
        log_name = self.__get_log_name()
        log_file = self.__get_log_path()
        if not log_name:
            return None
        handler = TimedRotatingFileHandler(log_file, when="D", backupCount=5)
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s][file:%(filename)s][lineno:%(lineno)d]'
            '[%(message)s]'  # [%(levelname)s]
        ))

        logging.basicConfig(level=self.level)
        logger = logging.getLogger(log_name)
        logger.addHandler(handler)

        return logger

    def __set_dbconnection(self):
        config = DATABASES.get(self.__db_name)
        conn = psycopg2.connect(**config)

        return conn.cursor()

    @property
    def user_agent(self):
        return self.random

