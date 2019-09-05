from datetime import datetime

from . import db


class BaseModel(object):
    """用于继承的类"""
    __table_args__ = {'schema': 'base'}  # 指定scheme
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())