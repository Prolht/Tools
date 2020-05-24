from werkzeug.security import generate_password_hash,check_password_hash # 转换密码用到的库
from flask_security import RoleMixin, UserMixin # 登录和角色需要继承的对象
from itsdangerous import TimedJSONWebSignatureSerializer as SignatureExpired, BadSignature,  Serializer

from ..config.default import DefaultConfig
from ..models import db


# 角色<-->用户，关联表
roles_users = db.Table(
    'role_user',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


# 角色表
class Role(db.Model, RoleMixin):
    __bind_key__ = 'user'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "<Role_id:{0}>".format(self.id)


class User(db.Model, UserMixin):
    __bind_key__ = 'user'
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    memo = db.Column(db.Text)
    # 多对多关联
    roles = db.relationship('Role', secondary='role_user', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return "<User_id:{0}>".format(self.id)

    @property
    def password(self):
        raise AttributeError("密码不允许读取")

    # 转换密码为hash存入数据库
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash,password)

    # 获取token，有效时间1天
    def generate_auth_token(self, expiration=DefaultConfig.EXPIRATION):
        s = Serializer(DefaultConfig.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(DefaultConfig.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature as e:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user
