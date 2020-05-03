from config.db import db


class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, doc=u'用户唯一标识')
    username = db.Column(db.String(32), nullable=False, doc=u'用户名')
    password = db.Column(db.String(32), nullable=False, doc=u'密码')
    role = db.Column(db.Integer, nullable=False, default=2, doc=u'身份标识 0, 1, 2')
    contacts = db.Column(db.String(64), nullable=False, default='', doc=u'联系方式')
    join_experiments = db.Column(db.String(128), nullable=False, default='', doc=u'学生参加的实验')

    class Role(object):
        """
        用户身份
        """
        MANAGER = 0  # 管理员
        TEACHER = 1  # 老师
        STUDENT = 2  # 学生

        __label__ = {
            MANAGER: u"管理员",
            TEACHER: u"教师",
            STUDENT: u"学生"
        }