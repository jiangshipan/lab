from sqlalchemy import func

from config.db import db


class Laboratory(db.Model):
    """
    实验室表
    """
    __tablename__ = 'laboratory'

    id = db.Column(db.Integer, primary_key=True, doc='唯一标识')
    name = db.Column(db.String(32), nullable=False, default='', doc='实验室名称')
    notice = db.Column(db.String(512), nullable=False, default='', doc=u'公告')
    devices = db.Column(db.String(512), nullable=False, default='', doc=u'设备')