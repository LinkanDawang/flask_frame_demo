from werkzeug.security import generate_password_hash, check_password_hash

from mars import db
from mars.models import BaseModel


class UsersModel(db.Model, BaseModel):
    """用户模型"""
    __tablename__ = 'test_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(127), nullable=False)
    mobile = db.Column(db.String(11), nullable=False, unique=True)
    realname = db.Column(db.String(32))
    id_char = db.Column(db.String(20), nullable=True)
    avatar_url = db.Column(db.String(128))

    @property
    def password(self):
        """不允许用户密码被读取"""
        raise AttributeError('不支持读取操作')

    @password.setter
    def password(self, value):
        """加密用户密码"""
        self.password_hash = generate_password_hash(value)

    def check_password_hash(self, value):
        """校验用户密码"""
        return check_password_hash(self.password_hash, value)

    def to_dict(self):
        pass

