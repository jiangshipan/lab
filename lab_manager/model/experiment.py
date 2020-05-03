from sqlalchemy import func

from config.db import db


class Experiment(db.Model):
    """
    实验表
    """
    __tablename__ = 'experiment'

    id = db.Column(db.Integer, primary_key=True, doc=u'唯一标识')
    name = db.Column(db.String(32), nullable=False, default='', doc=u'实验名称')
    remark = db.Column(db.String(512), nullable=False, default='', doc=u'实验备注')
    start_time = db.Column(db.DateTime, nullable=False, default=func.now(), doc=u'开始时间')
    end_time = db.Column(db.DateTime, nullable=False, default=func.now(), doc=u'结束时间')
    lab_no = db.Column(db.Integer, nullable=False, default=0, doc=u'实验室编号')
    teacher_id = db.Column(db.Integer, nullable=False, default=0, doc=u'教师id')
    status = db.Column(db.Integer, nullable=False, default=1, doc=u'是否审批通过')

    class Status(object):
        SUCCESS = 0  # 成功
        PROCESS = 1  # 审批中
        FAILED = 2  # 失败

        __label__ = {
            SUCCESS: "审批通过",
            PROCESS: "审批中",
            FAILED: "审批未通过"
        }