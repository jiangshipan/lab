from sqlalchemy import func

from config.db import db


class Email(db.Model):
    """
    收件箱表
    """
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True, doc=u'唯一标识')
    user_id = db.Column(db.Integer, nullable=False, doc=u'用户id')
    content = db.Column(db.String(512), nullable=False, doc=u'邮件内容')
    create_id = db.Column(db.Integer, nullable=False, doc=u'创建人')
    create_name = db.Column(db.String(32), nullable=False, doc=u'创建人姓名')
    create_time = db.Column(db.DateTime, nullable=False, default=func.now(), doc=u'创建时间')
    