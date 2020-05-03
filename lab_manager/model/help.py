from config.db import db


class Help(db.Model):
    """
    帮助表
    """
    __tablename__ = 'help'

    id = db.Column(db.Integer, primary_key=True, doc=u'唯一标识')
    lab_id = db.Column(db.Integer, nullable=False, default=0, doc=u'实验室id')
    question = db.Column(db.String(512), nullable=False, doc=u'问题')
    status = db.Column(db.Integer, nullable=False, doc=u'状态 0 已解决, 1未解决')

    class Status(object):
        """
        状态
        """
        SOLVED = 0  # 已解决
        UNRESOLVED = 1  # 未解决

        __labels__ = {
            SOLVED: "已处理",
            UNRESOLVED: "未处理"
        }
