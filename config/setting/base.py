import os
import redis
import logging

from pathlib import Path
from logging.handlers import RotatingFileHandler


# 项目路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 配置 日志
LOG_DIR = os.path.join(BASE_DIR, 'log')  # 日志文件路径
if not os.path.exists(LOG_DIR):  # 创建日志目录
    os.makedirs(LOG_DIR)
rf_handler = RotatingFileHandler(LOG_DIR+'/'+'err.log', maxBytes=1024*1024*5, backupCount=5)
rf_handler.setLevel(logging.ERROR)
rf_handler.setFormatter(logging.Formatter(
    '[%(asctime)s][file:%(filename)s][lineno:%(lineno)d]'
    '[%(levelname)s][%(message)s]'
))
logger = logging.getLogger('global')
logger.addHandler(rf_handler)


# app配置
class BaseConfig(object):
    # 盐值生成方法 1:import os,base64  2:SECRET_KEY=base64.b64encode(os.urandom(24))
    SECRET_KEY = '8uRT2ga9wxXvu3BAmuQDFXDdmTeEKWQg'

    # REDIS连接配置
    REDIS_HOST = '192.168.3.168'
    redis_PORT = 6379

    # Flask-Session配置
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=redis_PORT)
    PERMANENT_SESSION_LIFETIME = 86400*2

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'postgresql://leslie:comeoncg@192.168.3.168/flask_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 日志记录器
    LOGGER = logger

