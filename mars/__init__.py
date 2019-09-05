from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

from config.setting.base import BaseConfig
from mars.utils.common import RegexConverter


# 函数外部定义扩展，便于其他模块导入，延迟加载配置
db = SQLAlchemy()
redis_store = None
logger = None


def create_app(conf_obj=None):
    if conf_obj != BaseConfig:
        pass
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(conf_obj)

    # url自定义过滤器re(正则)
    app.url_map.converters['re'] = RegexConverter

    # 开启CSRF保护
    # CSRFProtect(app)

    # redis连接对象
    global redis_store, logger
    redis_store = conf_obj.SESSION_REDIS
    logger = conf_obj.LOGGER

    # flask默认session存储位置为浏览器，此方法可使session存储到redis中
    Session(app)

    # 数据库连接对象
    db.init_app(app)

    # 注册蓝图
    from mars.routes import api
    app.register_blueprint(api, url_prefix='/api/v_1_0')

    return app, db

