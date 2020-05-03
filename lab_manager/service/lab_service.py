from dao.laboratory_dao import LaboratoryDao
from model.help import Help
from config.db import db
import json

from model.laboratory import Laboratory


class LabService(object):
    """
    实验室服务
    """

    def get_all_labs(self):
        labs = LaboratoryDao.get_all_labs()
        res = []
        for lab in labs:
            devices = json.loads(lab.devices)
            device_infos = []
            for k, v in devices.items():
                device_infos.append('%s:%s ' % (k, v))
            res.append({
                'id': lab.id,
                'name': lab.name,
                'notice': lab.notice,
                'devices': ''.join(device_infos)
            })
        return res

    def add_help(self, lab_id, question):
        """
        添加反馈
        :return:
        """
        try:
            h = Help()
            h.lab_id = lab_id
            h.question = question
            h.status = Help.Status.UNRESOLVED
            db.session.add(h)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    def get_all_helps(self):
        helps = LaboratoryDao.get_all_helps()
        res = []
        # 查询所有实验室
        lab_ids = [_.lab_id for _ in helps]
        lab_infos = LaboratoryDao.get_lab_by_ids(lab_ids)
        lab_id2name = {_.id: _.name for _ in lab_infos}
        for h in helps:
            res.append({
                'id': h.id,
                'lab_name': lab_id2name.get(h.lab_id, '未知'),
                'question': h.question,
                'status': Help.Status.__labels__.get(h.status, '未知')
            })
        return res

    def do_helps(self, hid, status):
        h = LaboratoryDao.get_help_by_id(hid)
        try:
            h.status = status
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    def add_new_lab(self, info):
        try:
            lab = Laboratory()
            lab.name = info.get('name')
            lab.notice = info.get('notice')
            lab.devices = json.dumps(self.format_devices(info.get('devices')))
            db.session.add(lab)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception("请使用英文富符号")

    def update_lab_device(self, lab_id, devices):
        try:
            lab = LaboratoryDao.get_lab_by_ids([lab_id])[0]
            lab.devices = json.dumps(self.format_devices(devices))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception("请使用英文富符号")

    def format_devices(self, devices):
        res = {}
        devices = devices.split(',')
        for device in devices:
            device_list = device.split(':')
            res.update({
                device_list[0]: device_list[1]
            })
        return res


if __name__ == '__main__':
    LabService().format_devices('苹果: 10个, 香蕉: 5个')
